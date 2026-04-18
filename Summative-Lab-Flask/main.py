import argparse
import requests
from rich.console import Console
from rich.table import Table

console = Console()
BASE_URL = "http://127.0.0.1:5000/inventory"

def main():
    parser = argparse.ArgumentParser(description="Inventory Admin CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # List all products
    subparsers.add_parser("list", help="List all inventory items")

    # Add a product
    add_parser = subparsers.add_parser("add", help="Add new product")
    add_parser.add_argument("--name", required=True)
    add_parser.add_argument("--brand", required=True)
    add_parser.add_argument("--price", type=float, required=True)

    # Delete a product
    del_parser = subparsers.add_parser("delete", help="Delete a product")
    del_parser.add_argument("--id", required=True, help="Product ID/Barcode")

    # Edit/Update a product
    edit_parser = subparsers.add_parser("edit", help="Edit an existing product")
    edit_parser.add_argument("--id", required=True, help="The Code/ID of the product to edit")
    edit_parser.add_argument("--name", help="New name for the product")
    edit_parser.add_argument("--price", type=float, help="New price for the product")

    fetch_parser = subparsers.add_parser("fetch", help="Fetch product details via barcode")
    fetch_parser.add_argument("--barcode", required=True, help="The barcode to search")

    args = parser.parse_args()


    if args.command == "list":
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            products = response.json()
            table = Table(title="Current Inventory")
            table.add_column("ID/Code", style="blue")
            table.add_column("Name", style="cyan")
            table.add_column("Brand", style="green")
            table.add_column("Price", style="magenta")

            for p in products:
                table.add_row(p['code'], p['name'], p['brands'], f"${p['price']:.2f}")
            console.print(table)
        else:
            console.print("[red]Failed to fetch inventory.[/red]")

    elif args.command == "add":
        payload = {"name": args.name, "brands": args.brand, "price": args.price}
        response = requests.post(BASE_URL, json=payload)
        if response.status_code == 201:
            console.print(f"[green]Successfully added:[/green] {args.name}")
        else:
            console.print("[red]Error adding product.[/red]")

    elif args.command == "delete":
        response = requests.delete(f"{BASE_URL}/{args.id}")
        if response.status_code == 204:
            console.print(f"[yellow]Product {args.id} deleted.[/yellow]")
        else:
            console.print(f"[red]Error: Product not found.[/red]")

    #update
    elif args.command == "edit":
        payload = {}
        if args.name:
            payload["name"] = args.name
        if args.price is not None:
            payload["price"] = args.price

        if not payload:
            console.print("[yellow]No changes provided. Use --name or --price to update.[/yellow]")
            return

        response = requests.patch(f"{BASE_URL}/{args.id}", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            console.print(f"[green]Successfully updated product {args.id}:[/green]")
            console.print(f"Name: {data['name']} | Price: ${data['price']:.2f}")
        else:
            error = response.json().get("error", "Product not found")
            console.print(f"[red]Error:[/red] {error}")

    elif args.command == "fetch":
        response = requests.post(f"{BASE_URL}/fetch/{args.barcode}")
        if response.status_code == 201:
            data = response.json()
            console.print(f"[green]Fetched and added:[/green] {data['name']} ({data['brands']})")
        else:
            error = response.json().get("error", "Unknown error")
            console.print(f"[red]Error:[/red] {error}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()