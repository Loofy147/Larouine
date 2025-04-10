from .interfaces.cli_interface import EnhancedInterface
from .core.fusion_core import SmartFusionSystemPro

def main():
    fusion_system = SmartFusionSystemPro()
    interface = EnhancedInterface()
    
    try:
        interface.start_interactive_mode()
    except KeyboardInterrupt:
        print("\nSystem shutdown gracefully.")
    
    if fusion_system.config['auto_update']:
        fusion_system.check_for_updates()

if __name__ == "__main__":
    main()

from .core.evolution_loop import EvolutionLoop
from .interfaces.cli_interface import CLIInterface

def main():
    cli = CLIInterface()
    cli.start_interactive()
    
    # بدء حلقة التطور في الخلفية
    evolution = EvolutionLoop()
    evolution.start()