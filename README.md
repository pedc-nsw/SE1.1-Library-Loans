# Binary Bay High Library - Loans Management

This app is an internal tool for the library staff at Binary Bay High School.

## What it does

From the terminal behind the library desk, staff use this tool to:

- search the catalogue and see how many copies of a title are available
- check books out to students and take them back in
- see what is overdue and how much each student owes in fines
- email overdue notices to the students who have them
- add new titles by looking up a scanned ISBN
- upload a nightly loans report to the office

### Why it talks to outside services

Most of what this tool does is just reading and writing the database on this
machine. Three components are not, and each one needs an account somewhere else:

- **Email.** Overdue notices go out to students at their school email address.
  These are sent through the mail provider the school already pays for.

- **Catalogue lookup.** Searching our own shelves is just a database query on
  this machine. Adding a *new* book is not. Staff scan the barcode and the
  tool sends the ISBN out to a book data service, which sends back the title,
  author and category. That way our records match what every other library
  holds, and nobody has to type all of it by hand for each box of 60 that
  arrives.

- **Cloud storage.** The library terminal is a standalone machine behind the
  desk and is not on the office file share, so the nightly loans report
  cannot simply be saved to a folder the front office can open. Instead it is
  uploaded at 11:30pm to the school's cloud storage account, which the office
  already uses for this kind of handover, and pulled down the next morning.

## Setting it up

You need Python 3.9 or newer. Open a terminal in this folder & check with:

```
python --version
```

Then in the same terminal create the database:

```
python library.py setup
```

That loads the sample catalogue, students, and loans so there is something
to work with.

## You can now start browsing project files for secrets to complete the exercise! If you want to use the application, keep reading:

This is a simple CLI application with no GUI. If you want to use the
application, you can try running some of these commands from your terminal:

```
python library.py search macbeth         # search title and author
python library.py checkout 3 2201        # book 3 out to student 2201
python library.py return 3               # take book 3 back in
python library.py overdue                # overdue loans and fines
python library.py notify                 # email overdue notices
python library.py lookup 9780980874945   # look up a scanned ISBN
python library.py upload-report          # send the nightly report
```

The last three functions reach outside the school system. Add `--demo` to any
of them and the tool prints what it would have sent instead.

```
python library.py notify --demo
python library.py lookup 9780980874945 --demo
python library.py upload-report --demo
```

## What is in here

| File | What it is |
|------|------------|
| `library.py` | The command line interface, good starting point |
| `catalogue.py` | Catalogue search and ISBN lookup. |
| `loans.py` | Checking books in and out, overdue loans, fines. |
| `notices.py` | Overdue notice emails. |
| `reports.py` | Builds and uploads the nightly loans report. |
| `config.py` | Settings and connection details. |
| `db.py` | Database schema and connection handling. |
| `utils/hashing.py` | Password hashing for staff logins. |
| `deploy/` | Notes for setting up the library terminal. |
| `tests/` | Unit tests and shared test data. |
| `data/seed.json` | Sample catalogue and loans loaded during setup. |
| `requirements.txt` | Pinned package versions. Not needed to run the tool. |

## Tests

```
python -m unittest discover tests
```

---

## Installing a secret scanner

Step 2 of the exercise asks you to run a secret scanner over this project.
`gitleaks` is a single file. There is no installer, you do not need admin
rights, and it does not add anything to Python.

**Windows**

1. Go to https://github.com/gitleaks/gitleaks/releases
2. Download the file ending in `windows_x64.zip`. You may need to click the
"Show all X assets" at the bottom of newer releases. 
3. Right-click it, Extract All, and put `gitleaks.exe` into this project folder
4. Check it runs: `.\gitleaks.exe version`

**macOS and Linux**

1. From the same page, download the `darwin_x64` (Mac) or `linux_x64` (Linux)
   `.tar.gz`
2. Extract it and put `gitleaks` into this project folder
3. Make it runnable and check it: `chmod +x gitleaks` then `./gitleaks version`

Once it runs, there are two scans to do, and the difference between them
matters:

```
.\gitleaks detect --no-git --source .    # the files as they are right now
.\gitleaks detect                        # every version of every file, ever
```

On macOS and Linux the prefix is `./gitleaks` rather than `.\gitleaks`.

### If the school network blocks the download

Ask your teacher. They can download it once and put it on the shared drive or
a USB stick.

If you cannot get the tool at all, you can do a rough version by hand with
git, which you already have. Record what this approach misses - that is worth
saying in your answer to step 2.

Search the files as they are now:

```
git grep -n -i -E "password|secret|api_key|apikey|token"
```

Read the entire history of a single file, including lines that were deleted:

```
git log -p -- catalogue.py
```

In that output, a line starting with `-` was removed from the file at that
commit, and a line starting with `+` was added. Try it on each `.py` file in
turn.
