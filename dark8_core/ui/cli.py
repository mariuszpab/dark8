# DARK8 OS - CLI Interface
"""
Command-line interface for DARK8 OS agent.
"""

import asyncio

from dark8_core.agent import get_agent
from dark8_core.logger import logger
from dark8_core.nlp import get_nlp_engine


class CLIInterface:
    """CLI Agent interface"""

    BANNER = r"""
╔════════════════════════════════════════════════════════════════╗
║                   🖤 DARK8 OS - CLI Agent                      ║
║                Autonomous AI Operating System                  ║
║                                                                ║
║  Type 'help' for commands, 'exit' to quit                      ║
╚════════════════════════════════════════════════════════════════╝
    
    Examples:
      • zbuduj aplikację todo w Django
      • szukaj informacji o Machine Learning
      • przeanalizuj kod z pliku main.py
      • uruchom polecenie: ls -la
      • pokàż zawartość katalogu ./src
    """

    def __init__(self):
        self.nlp = get_nlp_engine()
        self.agent = get_agent()

    def show_banner(self):
        """Display welcome banner"""
        print(self.BANNER)

    def show_help(self):
        """Show help"""
        help_text = """
🖤 DARK8 OS - Available Commands:

NLP-Powered Commands (in Polish):
  • zbuduj / stwórz <app>        - Build application
  • szukaj <query>               - Search information
  • otwórz <url>                 - Open in browser
  • przeanalizuj <code>          - Analyze code
  • uruchom <command>            - Execute command

Direct Commands:
  • help                         - Show this help
  • status                        - Show system status
  • clear                         - Clear screen
  • exit / quit                   - Exit DARK8

Examples:
  agent> zbuduj aplikację todo w Django z bazą PostgreSQL
  agent> szukaj jak stworzyć REST API
  agent> uruchom: python main.py --help
  agent> otwórz https://github.com w przeglądarce
        """
        print(help_text)

    def show_status(self):
        """Show system status"""
        import psutil

        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory()

        print("\n📊 System Status:")
        print(f"  CPU: {cpu}%")
        print(f"  Memory: {mem.percent}%")
        print(f"  Available: {mem.available / 1024 / 1024:.1f} MB")
        print("\n📚 Agent:")
        print(f"  Memories: {len(self.agent.memory.conversation_history)}")
        print(f"  Tasks: {len(self.agent.memory.task_history)}")

    async def run(self):
        """Main CLI loop"""
        self.show_banner()

        while True:
            try:
                # Get user input
                user_input = input("\n🖤 agent> ").strip()

                if not user_input:
                    continue

                # Handle direct commands
                if user_input.lower() == "help":
                    self.show_help()
                    continue
                elif user_input.lower() == "status":
                    self.show_status()
                    continue
                elif user_input.lower() == "clear":
                    import os

                    os.system("clear" if os.name != "nt" else "cls")
                    continue
                elif user_input.lower() in ["exit", "quit", "stop"]:
                    logger.info("🖤 Goodbye!")
                    break

                # Process through NLP
                nlp_result = self.nlp.understand(user_input)

                # Check confidence
                if nlp_result["confidence"] < 0.2:
                    print(f"❌ Command not understood (confidence: {nlp_result['confidence']:.0%})")
                    print("   Type 'help' for available commands")
                    continue

                # Execute through agent
                logger.debug(
                    f"Intent: {nlp_result['intent']}, Confidence: {nlp_result['confidence']:.1%}"
                )

                response = await self.agent.process_command(user_input, nlp_result)
                print(f"\n✓ {response}")

            except KeyboardInterrupt:
                print("\n\n🖤 Agent interrupted. Type 'exit' to quit.")
            except Exception as e:
                logger.error(f"CLIError: {e}", exc_info=True)
                print(f"❌ Error: {e}")


async def main():
    """CLI main"""
    cli = CLIInterface()
    await cli.run()


if __name__ == "__main__":
    asyncio.run(main())
