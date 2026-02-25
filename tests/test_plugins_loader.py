import pytest
import dark8_mark01.plugins as plugins


def _write_module(path, name, content):
    p = path / f"{name}.py"
    p.write_text(content)
    return p


def test_load_all_plugins(tmp_path, monkeypatch, capsys):
    # create temp plugin modules: file, web, tools, core, extra
    content = """
import dark8_mark01.plugins as plugins
plugins._registered = getattr(plugins, '_registered', [])
plugins._registered.append('{name}')
"""
    names = ["file", "web", "tools", "core", "extra"]
    for n in names:
        _write_module(tmp_path, n, content.replace('{name}', n))

    # point package __path__ to tmp_path
    monkeypatch.setattr(plugins, "__path__", [str(tmp_path)])
    # call loader with explicit path (testable)
    plugins.load_plugins(paths=[str(tmp_path)], package_name=plugins.__name__)

    assert hasattr(plugins, "_registered")
    assert set(plugins._registered) == set(names)


def test_conflicting_plugin_names(tmp_path, monkeypatch):
    # create two dirs with same plugin name
    dir1 = tmp_path / "d1"
    dir2 = tmp_path / "d2"
    dir1.mkdir()
    dir2.mkdir()

    # both contain a module named 'dup'
    (dir1 / "dup.py").write_text("# dup1")
    (dir2 / "dup.py").write_text("# dup2")

    # set __path__ to include both directories
    monkeypatch.setattr(plugins, "__path__", [str(dir1), str(dir2)])
    with pytest.raises(RuntimeError):
        plugins.load_plugins(paths=[str(dir1), str(dir2)], package_name=plugins.__name__)


def test_registers_subplugins(tmp_path, monkeypatch):
    # plugin that registers subitems
    content = """
import dark8_mark01.plugins as plugins

def register():
    plugins._registered = getattr(plugins, '_registered', [])
    plugins._registered.extend(['parent', 'parent.child'])
"""
    _write_module(tmp_path, "parent", content)
    monkeypatch.setattr(plugins, "__path__", [str(tmp_path)])
    if hasattr(plugins, "_registered"):
        delattr(plugins, "_registered")
    plugins.load_plugins(paths=[str(tmp_path)], package_name=plugins.__name__)
    assert 'parent' in plugins._registered
    assert 'parent.child' in plugins._registered


def test_end_to_end_call_plugin_function(tmp_path, monkeypatch):
    content = """
import dark8_mark01.plugins as plugins

def do_work(x):
    return x * 2

def register():
    # expose function on package for simple E2E test
    setattr(plugins, 'do_work', do_work)
    plugins._registered = getattr(plugins, '_registered', [])
    plugins._registered.append('do_work_plugin')
"""
    _write_module(tmp_path, "do_work_plugin", content)
    monkeypatch.setattr(plugins, "__path__", [str(tmp_path)])
    plugins.load_plugins(paths=[str(tmp_path)], package_name=plugins.__name__)

    # cleanup
    if hasattr(plugins, "_registered"):
        delattr(plugins, "_registered")
    if hasattr(plugins, "do_work"):
        delattr(plugins, "do_work")

    plugins.load_plugins(paths=[str(tmp_path)], package_name=plugins.__name__)

    assert 'do_work_plugin' in plugins._registered
    assert hasattr(plugins, 'do_work')
    assert plugins.do_work(3) == 6


def test_plugin_without_register_is_ignored(tmp_path, monkeypatch, capsys):
    # module with no register()
    _write_module(tmp_path, "no_register", "# no register here")
    monkeypatch.setattr(plugins, "__path__", [str(tmp_path)])
    plugins.load_plugins(paths=[str(tmp_path)], package_name=plugins.__name__)
    captured = capsys.readouterr()
    assert "nie ma funkcji register()" in captured.out


def test_plugin_with_import_error(tmp_path, monkeypatch, capsys):
    # module that raises at import time
    _write_module(tmp_path, "bad", "raise RuntimeError('boom')")
    monkeypatch.setattr(plugins, "__path__", [str(tmp_path)])
    plugins.load_plugins(paths=[str(tmp_path)], package_name=plugins.__name__)
    captured = capsys.readouterr()
    assert "Błąd ładowania bad" in captured.out
