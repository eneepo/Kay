// tasklist-web — a tiny task list. Starter for the Kay hands-on lab.
// No build step, no dependencies: open index.html in a browser.

const tasks = []; // { text, done }

const form = document.getElementById("add-form");
const input = document.getElementById("task-input");
const list = document.getElementById("task-list");
const empty = document.getElementById("empty");

function render() {
  list.innerHTML = "";
  for (const [i, task] of tasks.entries()) {
    const li = document.createElement("li");
    if (task.done) li.classList.add("done");

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = task.done;
    checkbox.id = `task-${i}`;
    checkbox.addEventListener("change", () => {
      task.done = checkbox.checked;
      render();
    });

    const label = document.createElement("label");
    label.htmlFor = `task-${i}`;
    label.textContent = task.text;

    li.append(checkbox, label);
    list.append(li);
  }
  empty.hidden = tasks.length > 0;
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return; // ignore empty submissions
  tasks.push({ text, done: false });
  input.value = "";
  render();
});

render();
