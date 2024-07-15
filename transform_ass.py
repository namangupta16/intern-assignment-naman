import re

def read_ass_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.readlines()

def write_ass_file(filename, lines):
    with open(filename, 'w', encoding='utf-8') as file:
        file.writelines(lines)

def process_events(input_lines):
    events_start = False
    events = []

    for line in input_lines:
        if line.strip().startswith("[Events]"):
            events_start = True
        if events_start and line.startswith("Dialogue:"):
            events.append(line.strip())

    return events

def add_context_to_events(events):
    updated_events = []

    for i, event in enumerate(events):
        prev_event = events[i-1] if i > 0 else "Dialogue: 0,0:00:00.00,0:00:00.00,Default,,0,0,0,..."
        next_event = events[i+1] if i < len(events) - 1 else "Dialogue: 0,0:00:00.00,0:00:00.00,Default,,0,0,0,..."

        prev_text = extract_text(prev_event)
        current_text = extract_text(event)
        next_text = extract_text(next_event)

        new_text = f"{prev_text} | {current_text} | {next_text}"
        updated_event = replace_text_in_event(event, new_text)
        updated_events.append(updated_event)

    return updated_events

def extract_text(event):
    match = re.search(r'Dialogue:.*?,.*?,.*?,.*?,(.*)', event)
    if match:
        return match.group(1)
    return "..."

def replace_text_in_event(event, new_text):
    return re.sub(r'(Dialogue:.*?,.*?,.*?,.*?,).*', r'\1' + new_text, event)

def update_ass_file(input_lines, updated_events):
    events_start = False
    output_lines = []
    event_index = 0

    for line in input_lines:
        if line.strip().startswith("[Events]"):
            events_start = True
            output_lines.append(line)
            continue
        if events_start and line.startswith("Dialogue:"):
            output_lines.append(updated_events[event_index] + '\n')
            event_index += 1
        else:
            output_lines.append(line)

    return output_lines

def main():
    input_filename = "input_subtitles.ass"
    output_filename = "output_subtitles.ass"

    input_lines = read_ass_file(input_filename)
    events = process_events(input_lines)
    updated_events = add_context_to_events(events)
    output_lines = update_ass_file(input_lines, updated_events)
    write_ass_file(output_filename, output_lines)

if __name__ == "__main__":
    main()
