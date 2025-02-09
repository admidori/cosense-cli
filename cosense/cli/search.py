import curses
import sys
from turtle import st
import cosense
from functools import partial
import locale
import unicodedata
import datetime
import threading
import math
import time
import json

def search(args):
    locale.setlocale(locale.LC_ALL, "")
    curses.wrapper(partial(select_pages, args = args))

def read_page(page, text, stdscr):
    stdscr.clear()

    created_date = datetime.datetime.fromtimestamp(int(page["created"]))
    created = created_date.strftime("%Y-%m-%d")
    updated_date = datetime.datetime.fromtimestamp(int(page["updated"]))
    updated = updated_date.strftime("%Y-%m-%d")

    text = str(text)
    start_num = 0
    while True:
        height, width = stdscr.getmaxyx()
        stdscr.addstr(0, 0, "quit: 'q' / move page: 'j' or 'k'", curses.A_REVERSE)

        stdscr.addstr(1, 0, f"Title: {page['title']}")
        stdscr.addstr(2, 0, f"Created: {created}")
        stdscr.addstr(3, 0, f"Updated: {updated}")
        stdscr.addstr(4, 0, f"Views: {page['views']}")
        stdscr.addstr(5, 0, "=" * 50)

        appear_text = text.split("\n")[start_num:start_num + height - 7]
        stdscr.addstr(6, 0, "\n".join(appear_text))

        key = stdscr.getkey()

        if key == "q":
            break
        elif key == "k":
            start_num = max(0, start_num - (height - 7))
            stdscr.clear()
        elif key == "j":
            start_num = min(len(text.split("\n")), start_num + (height - 7))
            stdscr.clear()
        else:
            stdscr.addstr(0, 0, f"Unknown key: {key}", curses.A_REVERSE)

        stdscr.refresh()

def unicodeLen(text):
    count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in 'FWA':
            count += 2
        else:
            count += 1
    return count

def ljust(string,length):
    for char in string:
        if unicodedata.east_asian_width(char) in ('F', 'W', 'A'):
            length -= 2
        else:
            length -= 1
    return string + ' ' * length

def fetch(lock, client, project, page_total, pages, texts):
    for i in range(page_total):
        fetch_page(lock, client, project, pages, i*100)
        time.sleep(0.5)
    
    cnt = 0
    for page in pages:
        fetch_text(lock, client, project, page, texts)
        cnt += 1
        if cnt % 10 == 0:
            time.sleep(5)

def fetch_page(lock, client, project, pages, skip_count):
    page = client.get(project, skip=skip_count, limit=100)
    with lock:
        pages.extend(page["pages"])

def fetch_text(lock, client, project, page, texts):
    text = client.get(project + "/" + page["title"] + "/text")
    with lock:
        texts.append(text)

def select_pages(stdscr, args):
    pages = []
    texts = []
    page_number = 0
    selected = 1
    IS_FETCHED = False

    # Initialize client
    if args.auth is None:
        client = cosense.Client()
    else:
        client = cosense.Client(sid=args.auth)

    # Fetch the first page to get the total number of pages
    pj = client.get(args.project, limit=0)
    page_total_pj = math.ceil(int(pj["count"]) / 100)

    curses.curs_set(0)
    stdscr.keypad(1)

    # Fetch pages and texts
    lock = threading.Lock()
    thread = threading.Thread(target=fetch, args=(lock, client, args.project, page_total_pj, pages, texts), daemon=True)
    thread.start()

    time.sleep(1)
    stdscr.clear()

    while True:
        # Check terminal size
        height, width = stdscr.getmaxyx()
        if height < 10 or width < 50:
            print("Please resize the terminal to at least 50x10")
            sys.exit(1)
        DISPLAY_PAGES = 45
        page_total = math.ceil((page_total_pj * 100) / DISPLAY_PAGES)

        # Menubar
        len_pages = len(pages)
        len_texts = len(texts)

        download_status = ""
        if len_pages < page_total:
            download_status = "Downloading pages: " + "-"*int((len_pages + 1) / 10) + " "*int((page_total / 10) - ((len_pages + 1) / 10))
        elif len_texts < len_pages:
            download_status = "Donwloading texts: " + "-"*int((len_texts + 1) / 10) + " "*int((len_pages / 10) - ((len_texts + 1) / 10))
        else:
            IS_FETCHED = True
            download_status = "'J' to output the project to json file"
        stdscr.addstr(height - 2, 0, f"Project: {args.project} Page: {page_number+1}/{page_total} {download_status}", curses.A_REVERSE)
        stdscr.addstr(height - 1, 0, "quit: 'q' / read: 'Enter' / select article: 'j' or 'k' / move page: 'h' or 'l'", curses.A_REVERSE)
        # Infobar
        infobar = "   " + ljust("Title", 40) + ljust("Created", 15) + ljust("Updated", 15)
        stdscr.addstr(1, 0, infobar, curses.A_BOLD)
        
        with lock:
            split_pages = pages[DISPLAY_PAGES*page_number:DISPLAY_PAGES*(page_number+1)]

        # Handle key input
        key = stdscr.getkey()
        if key == "k":
            selected = max(1, selected - 1)
        elif key == "j":
            selected = min(len(pages), selected + 1)
        elif key == "h":
            page_number = max(0, page_number - 1)
            selected = 1
        elif key == "l":
            page_number = min(page_total - 1, page_number + 1)
            selected = 1
        elif key == "\n":
            if IS_FETCHED:
                pagenum = DISPLAY_PAGES * page_number + selected - 1
                read_page(pages[selected - 1], texts[pagenum], stdscr)
                stdscr.clear()
        elif key == "q":
            sys.exit(0)
        elif key == "J":
            with open("output.json", "w") as f:
                output_json = {
                    "name": "",
                    "displayName":"",
                    "exported":"",
                    "users":[{
                        "id":"",
                        "name":"",
                        "displayName":"",
                        "email":""
                    }],
                    "pages": []
                }
                for page in pages:
                    t = str(texts[pages.index(page)])
                    new_text = t.split("\n")

                    new_page = {
                        "title": page["title"],
                        "created": page["created"],
                        "updated": page["updated"],
                        "id": page["id"],
                        "views": page["views"],
                        "lines": new_text
                    }
                    output_json["pages"].append(new_page)
                f.write(json.dumps(output_json, indent=2, ensure_ascii=False))
            sys.exit(0)
        else:
            stdscr.addstr(0, 0, f"Unknown key: {key}", curses.A_REVERSE)

        for i, page in enumerate(split_pages):
            title = page["title"]
            created_date = datetime.datetime.fromtimestamp(int(page["created"]))
            created = created_date.strftime("%Y-%m-%d")
            updated_date = datetime.datetime.fromtimestamp(int(page["updated"]))
            updated = updated_date.strftime("%Y-%m-%d")

            if unicodeLen(title) > 30:
                count_char = 0
                count_total = 0
                for c in title:
                    if count_total > 30:
                        break
                    count_char += 1
                    if unicodedata.east_asian_width(c) in 'FWA':
                        count_total += 2
                    else:
                        count_total += 1
                title = title[:count_char] + "..."
            title = ljust(title, 40)
            created = ljust(created, 15)
            updated = ljust(updated, 15)
            formatted = f"{title}{created}{updated}"

            i = i + 1
            if i == selected:
                stdscr.addstr(i + 1, 0, "-> " + formatted)
            else:
                stdscr.addstr(i + 1, 0, "   " + formatted)

        stdscr.refresh()
