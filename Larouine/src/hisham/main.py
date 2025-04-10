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