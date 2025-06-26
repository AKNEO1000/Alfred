import webbrowser
import random
import sys

# Try to import the wikipedia library.
# If it's not installed, provide instructions to the user.
try:
    import wikipedia
except ImportError:
    print("The 'wikipedia' library is not installed.")
    print("Please install it using: pip install wikipedia")
    print("You can still use other features of the chatbot.")
    wikipedia = None # Set wikipedia to None so we can check for it later

def open_website(url):
    """Opens a given URL in the default web browser."""
    try:
        webbrowser.open_new_tab(url)
        print(f"Opening {url} in your browser.")
    except Exception as e:
        print(f"Could not open the website: {e}")

def google_search(query):
    """Performs a Google search for the given query."""
    search_url = f"https://www.google.com/search?q={query}"
    open_website(search_url)

def wikipedia_search(query):
    """Performs a Wikipedia search for the given query and prints a summary."""
    if wikipedia is None:
        print("The 'wikipedia' library is not available. Cannot perform Wikipedia searches.")
        return

    try:
        print(f"Searching Wikipedia for '{query}'...")
        # Get a summary of the Wikipedia page
        summary = wikipedia.summary(query, sentences=2)
        print("\n--- Wikipedia Summary ---")
        print(summary)
        print("-------------------------\n")
        # Offer to open the full page
        print(f"You can find the full article here: https://en.wikipedia.org/wiki/{query.replace(' ', '_')}")
    except wikipedia.exceptions.DisambiguationError as e:
        print(f"Your query '{query}' is ambiguous. Please be more specific. Possible options: {e.options[:5]}...")
    except wikipedia.exceptions.PageError:
        print(f"Could not find a Wikipedia page for '{query}'.")
    except Exception as e:
        print(f"An error occurred during Wikipedia search: {e}")

def tell_joke():
    """Tells a random joke from a predefined list."""
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Did you hear about the mathematician who was afraid of negative numbers? He'd stop at nothing to avoid them.",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "What do you call a fake noodle? An impasta!"
    ]
    print(random.choice(jokes))

class TodoList:
    """Manages a simple to-do list."""
    def __init__(self):
        self.tasks = []
        self.next_id = 1

    def add_task(self, task):
        """Adds a new task to the list."""
        self.tasks.append({"id": self.next_id, "task": task, "completed": False})
        print(f"Task '{task}' added with ID {self.next_id}.")
        self.next_id += 1

    def view_tasks(self):
        """Displays all tasks in the list."""
        if not self.tasks:
            print("Your to-do list is empty!")
            return

        print("\n--- Your To-Do List ---")
        for t in self.tasks:
            status = "[X]" if t["completed"] else "[ ]"
            print(f"{status} ID {t['id']}: {t['task']}")
        print("-----------------------\n")

    def complete_task(self, task_id):
        """Marks a task as completed."""
        try:
            task_id = int(task_id)
            found = False
            for t in self.tasks:
                if t["id"] == task_id:
                    if t["completed"]:
                        print(f"Task ID {task_id} is already completed.")
                    else:
                        t["completed"] = True
                        print(f"Task ID {task_id} '{t['task']}' marked as complete.")
                    found = True
                    break
            if not found:
                print(f"Task with ID {task_id} not found.")
        except ValueError:
            print("Invalid task ID. Please enter a number.")

    def delete_task(self, task_id):
        """Deletes a task from the list."""
        try:
            task_id = int(task_id)
            initial_len = len(self.tasks)
            self.tasks = [t for t in self.tasks if t["id"] != task_id]
            if len(self.tasks) < initial_len:
                print(f"Task ID {task_id} deleted.")
            else:
                print(f"Task with ID {task_id} not found.")
        except ValueError:
            print("Invalid task ID. Please enter a number.")


def display_help():
    """Displays available commands."""
    print("\n--- Chatbot Commands ---")
    print("  open <URL>           - Opens the specified URL (e.g., 'open https://www.google.com')")
    print("  google <query>       - Searches Google for the given query (e.g., 'google weather today')")
    print("  wikipedia <query>    - Searches Wikipedia for the given query (e.g., 'wikipedia Eiffel Tower')")
    print("  joke                 - Tells a random joke")
    print("  todo add <task>      - Adds a task to your to-do list (e.g., 'todo add Buy groceries')")
    print("  todo view            - Shows your current to-do list")
    print("  todo complete <ID>   - Marks a task as complete (e.g., 'todo complete 1')")
    print("  todo delete <ID>     - Deletes a task from the list (e.g., 'todo delete 2')")
    print("  help                 - Displays this help message")
    print("  exit / quit          - Exits the chatbot")
    print("------------------------\n")

def main():
    """Main function to run the chatbot."""
    print("Hello! I'm your simple Python chatbot. Type 'help' for commands.")
    todo_list = TodoList()

    while True:
        user_input = input("You: ").strip().lower()

        if user_input in ["exit", "quit"]:
            print("Goodbye!")
            break
        elif user_input == "help":
            display_help()
        elif user_input.startswith("open "):
            url = user_input[len("open "):].strip()
            if url:
                # Add http:// if not present for basic URL validity
                if not url.startswith(("http://", "https://")):
                    url = "http://" + url
                open_website(url)
            else:
                print("Please provide a URL to open. Example: 'open https://www.example.com'")
        elif user_input.startswith("google "):
            query = user_input[len("google "):].strip()
            if query:
                google_search(query)
            else:
                print("Please provide a query for Google search. Example: 'google latest news'")
        elif user_input.startswith("wikipedia "):
            query = user_input[len("wikipedia "):].strip()
            if query:
                wikipedia_search(query)
            else:
                print("Please provide a query for Wikipedia search. Example: 'wikipedia dogs'")
        elif user_input == "joke":
            tell_joke()
        elif user_input.startswith("todo add "):
            task = user_input[len("todo add "):].strip()
            if task:
                todo_list.add_task(task)
            else:
                print("Please provide a task to add. Example: 'todo add Finish report'")
        elif user_input == "todo view":
            todo_list.view_tasks()
        elif user_input.startswith("todo complete "):
            task_id_str = user_input[len("todo complete "):].strip()
            if task_id_str:
                todo_list.complete_task(task_id_str)
            else:
                print("Please provide the ID of the task to complete. Example: 'todo complete 1'")
        elif user_input.startswith("todo delete "):
            task_id_str = user_input[len("todo delete "):].strip()
            if task_id_str:
                todo_list.delete_task(task_id_str)
            else:
                print("Please provide the ID of the task to delete. Example: 'todo delete 2'")
        else:
            print("I didn't understand that command. Type 'help' to see what I can do.")

if __name__ == "__main__":
    main()
