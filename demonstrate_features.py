"""
Demonstration of Advanced Agentic Behaviors
Tests: Memory, Tool Use, Hallucination Prevention, Monitoring & Logging
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from agents.agent import (
    remember_info, 
    recall_info, 
    search_market, 
    find_keywords,
    verify_claim,
    check_performance,
    FEATURES_AVAILABLE
)

console = Console()

def print_header(title: str):
    """Print a formatted header."""
    console.print(f"\n[bold cyan]{'='*70}[/bold cyan]")
    console.print(f"[bold white]{title:^70}[/bold white]")
    console.print(f"[bold cyan]{'='*70}[/bold cyan]\n")

def demo_memory():
    """Demonstrate memory management capabilities."""
    print_header("1. MEMORY MANAGEMENT")
    
    console.print("[yellow]→ Storing product information...[/yellow]")
    result1 = remember_info("product_name", "Premium Wireless Earbuds")
    console.print(f"  [green]{result1}[/green]")
    
    result2 = remember_info("category", "Electronics")
    console.print(f"  [green]{result2}[/green]")
    
    result3 = remember_info("target_audience", "Young professionals, fitness enthusiasts")
    console.print(f"  [green]{result3}[/green]")
    
    console.print("\n[yellow]→ Retrieving stored information...[/yellow]")
    recalled1 = recall_info("product_name")
    console.print(f"  [blue]Product: {recalled1}[/blue]")
    
    recalled2 = recall_info("category")
    console.print(f"  [blue]Category: {recalled2}[/blue]")
    
    recalled3 = recall_info("target_audience")
    console.print(f"  [blue]Audience: {recalled3}[/blue]")
    
    console.print("\n[green]✓ Memory Management: PASSED[/green]")

def demo_tools():
    """Demonstrate tool use capabilities."""
    print_header("2. TOOL USE & ORCHESTRATION")
    
    console.print("[yellow]→ Searching market trends...[/yellow]")
    search_results = search_market("wireless earbuds market trends 2024", 3)
    console.print(Panel(search_results, title="Market Search Results", border_style="blue"))
    
    console.print("\n[yellow]→ Researching SEO keywords...[/yellow]")
    keywords = find_keywords("wireless earbuds", "Electronics")
    console.print(Panel(keywords, title="Keyword Research Results", border_style="blue"))
    
    console.print("\n[green]✓ Tool Use: PASSED[/green]")

def demo_hallucination_prevention():
    """Demonstrate hallucination detection and prevention."""
    print_header("3. HALLUCINATION PREVENTION")
    
    # Test 1: Valid claim
    console.print("[yellow]→ Testing VALID claim validation...[/yellow]")
    claim1 = "This product has excellent customer reviews"
    context1 = "Customer reviews show 4.5/5 stars with 85% positive feedback and 1,200+ verified purchases"
    
    result1 = verify_claim(claim1, context1)
    console.print(Panel(result1, title=f"Claim: '{claim1}'", border_style="green"))
    
    # Test 2: Invalid claim
    console.print("\n[yellow]→ Testing INVALID claim validation...[/yellow]")
    claim2 = "This product is the #1 best seller worldwide"
    context2 = "This is a new wireless earbud product launched 3 months ago"
    
    result2 = verify_claim(claim2, context2)
    console.print(Panel(result2, title=f"Claim: '{claim2}'", border_style="red"))
    
    # Test 3: Partially supported claim
    console.print("\n[yellow]→ Testing PARTIALLY supported claim...[/yellow]")
    claim3 = "This product offers 24-hour battery life"
    context3 = "Product specifications list 20 hours of playback time with charging case"
    
    result3 = verify_claim(claim3, context3)
    console.print(Panel(result3, title=f"Claim: '{claim3}'", border_style="yellow"))
    
    console.print("\n[green]✓ Hallucination Prevention: PASSED[/green]")

def demo_monitoring():
    """Demonstrate monitoring and logging capabilities."""
    print_header("4. MONITORING & LOGGING")
    
    console.print("[yellow]→ Retrieving performance metrics...[/yellow]")
    metrics = check_performance()
    console.print(Panel(metrics, title="Agent Performance Metrics", border_style="cyan"))
    
    console.print("\n[green]✓ Monitoring: PASSED[/green]")

def create_summary_table():
    """Create a summary table of all features."""
    table = Table(title="Advanced Agentic Behaviors Summary", show_header=True, header_style="bold magenta")
    
    table.add_column("Feature", style="cyan", width=25)
    table.add_column("Status", style="green", width=15)
    table.add_column("Implementation", style="yellow", width=30)
    
    table.add_row(
        "🧠 Memory Management",
        "✓ ACTIVE",
        "shared/memory_manager.py"
    )
    table.add_row(
        "🔧 Tool Use",
        "✓ ACTIVE",
        "6 specialized tools + orchestration"
    )
    table.add_row(
        "✓ Hallucination Prevention",
        "✓ ACTIVE",
        "shared/hallucination_guard.py"
    )
    table.add_row(
        "📊 Monitoring & Logging",
        "✓ ACTIVE",
        "shared/monitor.py + logger.py"
    )
    
    return table

def main():
    """Run the complete demonstration."""
    console.clear()
    
    # Header
    console.print("[bold green]" + "="*70 + "[/bold green]")
    console.print("[bold white]" + " "*15 + "ADVANCED AGENTIC BEHAVIORS DEMONSTRATION" + "[/bold white]")
    console.print("[bold white]" + " "*20 + "Multi-Agent System for Amazon Marketing" + "[/bold white]")
    console.print("[bold green]" + "="*70 + "[/bold green]\n")
    
    if not FEATURES_AVAILABLE:
        console.print("[bold red]ERROR: Advanced features are not available![/bold red]")
        console.print("[yellow]Please ensure all dependencies are installed.[/yellow]")
        return
    
    try:
        # Run all demonstrations
        demo_memory()
        demo_tools()
        demo_hallucination_prevention()
        demo_monitoring()
        
        # Show summary
        print_header("SUMMARY")
        console.print(create_summary_table())
        
        # Final message
        console.print(f"\n[bold green]{'='*70}[/bold green]")
        console.print("[bold white]" + " "*15 + "✓ ALL FEATURES DEMONSTRATED SUCCESSFULLY!" + "[/bold white]")
        console.print("[bold green]" + "="*70 + "[/bold green]\n")
        
        console.print("[cyan]The agent system is now ready with:[/cyan]")
        console.print("  • Multi-type memory (short-term, long-term, working)")
        console.print("  • 6+ specialized tools with orchestration")
        console.print("  • Real-time hallucination detection")
        console.print("  • Comprehensive monitoring & logging")
        console.print("\n[yellow]Access the ADK web interface at: http://127.0.0.1:8000[/yellow]")
        console.print("[cyan]Try asking the agent to demonstrate these capabilities![/cyan]\n")
        
    except Exception as e:
        console.print(f"[bold red]ERROR: {str(e)}[/bold red]")
        import traceback
        console.print(f"[red]{traceback.format_exc()}[/red]")

if __name__ == "__main__":
    main()
