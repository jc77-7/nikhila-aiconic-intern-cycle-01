# VS Code Debugging Notes

## Shortcuts
- `F5`: Start Debugging
- `Shift + F5`: Stop Debugging
- 'F6' : Pause
- `F9`: Toggle Breakpoint
- `F10`: Step Over
- `F11`: Step Into
- `Shift + F11`: Step Out
- 'ctrl + shift + F5' : Restart

## Debugging Tips
- Use **Watch** to monitor variables
- Use **Call Stack** to trace execution flow
- Add **Conditional Breakpoints**: Right-click a breakpoint → Edit Condition

| Term               | Meaning                                                                      |
| ------------------ | ---------------------------------------------------------------------------- |
| **Bug**            | An error or unexpected behavior in your code                                 |
| **Breakpoint**     | A marker that tells the debugger to pause your program at a specific line    |
| **Step Over**      | Run the next line of code, skipping over function details                    |
| **Step Into**      | Enter into the function being called on that line                            |
| **Step Out**       | Finish running the current function and return to where it was called        |
| **Call Stack**     | Shows which functions are currently running and how they were called         |
| **Watch**          | Lets you monitor a variable’s value as the program runs                      |
| **Locals/Globals** | Shows the current variables inside and outside the function you're debugging |

## Example Bug and Debug

def greet():
    message = "Hello"
    return messagee  # Bug: typo in variable name

print(greet())

## Debugging Steps:
1. Set breakpoint at return messagee.
2. Start debugger.
3. You’ll see a NameError.
4. Hover or check the Variables panel — messagee is undefined.
5. Fix to return message.

## What is launch.json?
- launch.json is a VS Code configuration file used to define how your app should run or debug.
- It's created when you click “Run and Debug” → “create a launch.json file”

"type": "python",
"request": "launch"
 --- This tells VS Code to launch a Python script.

 | What to Use            | Why                                      |
| ---------------------- | ---------------------------------------- |
| `"args"`               | Pass inputs for testing (e.g. city name) |
| `"env"`                | Set API keys for debugging               |
| `"stopOnEntry"`        | Pause on first line to inspect early     |
| `"integratedTerminal"` | For clean output + keyboard input        |
| Multiple configs       | Quickly test different scenarios         |
