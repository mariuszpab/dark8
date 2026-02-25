<script lang="ts">
    import { onMount } from "svelte";
    let logs: string[] = [];
    onMount(() => {
        logs.push("Agent panel ready");
    });
</script>

<div style="padding:8px; display:flex; flex-direction:column; height:100%;">
    <h3 style="margin:0 0 8px 0; padding:8px; border-bottom:1px solid #eee;">
        Agent
    </h3>
    <div style="flex:1; overflow:auto; padding:8px; background:#fafafa">
        {#each logs as l}
            <div
                style="font-family:monospace; font-size:12px; margin-bottom:6px;"
            >
                {l}
            </div>
        {/each}
    </div>
</div>
