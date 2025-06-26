import webbrowser
import random
import sys

# If the wikipedia library is not installed, system warns user.
try:
    import wikipedia
except ImportError:
    print("The 'wikipedia' library is not installed.")
    print("Please install it using: pip install wikipedia")
    print("You can still use other features of the chatbot.")
    wikipedia = None 

name = "Alfred" # user can change this later

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
        "What do you call a fake noodle? An impasta!",
	"Why was the frog late to work? because his car got toad."
    ]
    print(random.choice(jokes))

class TodoList:
    # simple to-do-list
    def __init__(self):
        self.tasks = []
        self.next_id = 1

    def add_task(self, task):
        """Adds a new task to the list."""
        self.tasks.append({"id": self.next_id, "task": task, "completed": False})
        print(f"Task '{task}' added with ID {self.next_id}.")
        self.next_id += 1

    def view_tasks(self):
        # to view a task
        if not self.tasks:
            print("Your to-do list is empty!")
            return

        print("\n--- Your To-Do List ---")
        for t in self.tasks:
            status = "[X]" if t["completed"] else "[ ]"
            print(f"{status} ID {t['id']}: {t['task']}")
        print("-----------------------\n")

    def complete_task(self, task_id):
        # to mark a task as complete
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
        # deletes a task
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


def help():
	help_message = f"""Hello, I am {name}, 
I can do a variety of tasks, such as:

1. Open websites -> for example, type: open youtube
2. Google for things -> for example, type : google The dark knight
3. Search on Wikipedia ->for example, type: wikipedia Hayden Christensen
4. Tell a joke -> for example, type: tell me a joke
5. Manage your to-do-list-> Here are the commands to:
				Add a task to your list -> todo add "task", each task has an ID number.
				View your tasks -> todo view
				Remove a task -> todo delete "ID number" 
				Mark a task as complete -> todo complete 'task ID number'
To exit, press: CTRL + C
 """
	print(help_message)
def main():
    # Main function for the chatbot.
    print(f"Hello! I'm {name}. Type 'help' for commands. To exit, press CTRL + C")
    todo_list = TodoList()

    while True:
        user_input = input("You: ").strip().lower()

        if "help" in user_input:
            help()

         # browsing, wikipedia: (online)
        elif user_input.startswith("open "):
            url = user_input[len("open "):].strip()
            if url:
                # Add http:// if not present for basic URL validity
                if not url.startswith(("http://", "https://")):
                    url = "http://" + url + ".com"
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


	# to-do-list:
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
         # responses:
        elif "joke" in user_input:
            tell_joke()
        elif "who are you" in user_input:
          print(f"I am {name}, your personal assistant")
        elif any(phrase in user_input for phrase in ["how are you", "are you good", "are you ok"]):
            status_responses = ['I\'m doing wonderful!', 'I\'m doing great, I\'m sure you are too!', "I'm doing fantastic!", 'I\'m always trying to do better!', 'Glad you asked, I\'m doing great!']
            print(random.choice(status_responses))
        elif any(greeting in user_input for greeting in ["hi", "hello", "hey"]):
            hello_responses = ["Hi!", "Hello!", "Hey!"]
            print(random.choice(hello_responses))


        else:
            print("I didn't understand that command. Type 'help' to see what I can do.")
        
if __name__ == "__main__":
    main()
