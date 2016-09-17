# media_work_queue
let's you build a queue of tasks to perform various operations

## Usage
1. You will build your work queue as a series of commands in `media_work_queue.py`.
2. There are various helper methods defined in the `Helpers` section for common scenarios.
3. Script out your work queue in the `Start Here` section.  There is already an example queue scripted there which you can use as a guide but should delete when you make your own queue.
4. Save the file and exit.
5. From the command line `python media_work_queue.py`
6. Your queue should now run to completetion.  INFO level messages will appear in the command prompt and DEBUG level info is available in the log file.  At the end of a run the script will log out any jobs that failed.

## Windows Install steps

1. Python 2.7
2. Pip https://pip.pypa.io/en/latest/installing/
3. Open a command prompt in the project directory
4. `virtualenv venv`
5. `venv\Scripts\activate` (run deactivate to end)
3. pip install -r requirements.txt

## Expected File Structures

TV Shows should be organized as follows:
```
Some Show 1
  |- Season 01
    |- Episode 01.mkv
  |- Season 02
    |- Episode 01.mkv
Some Show 2
  |- Season 01
    |- Episode 01.mkv
  |- Season 02
    |- Episode 01.mkv
```

Movies should be organized as follows:
```
Movie 1
  |- Featurette
    |- Trailer 01.mkv
  |- Movie 1.mkv
Movie 2
  |- Movie 2.mkv
```

## Customize

### media_work_queue.py
* **Logging** - You can customize the logging level and handlers in the `Logging` section.

### convertMKV.py
* **Featurette** - If you name your Featurette folder something else, you can set that property under the `Keywords` section.
* **Output Directory** - When converting, to modify the output location change the properties under the `Paths` section. When you convert a movie or tv show it is expected that you are converting from location A (the path you pass in) to location B (hardcoded property).  If you would like to change this behaviour then you will need to modify `convertMKV.py`.
* **Handbrake Path** - Set the path to your Handbrake.exe under the `Constants` section.
*  **Preset Profiles** - By default the Handbrake profile is set to 'High Profile', you cna modify this in the `Commands` section.

### zip_files.py
* **7z Path** - Set the path to your 7zip.exe under the `Constants` section.
* **7z Password** - If you use a password to encrypt/decrypt your archives then you can set the password in the `Constants` section.
* **Commands** - The individual commands that are used can be modified in the `Commands` section.  For instance, if you do not use a password to encrypt/decrypt archive files then you could remove the `-p{}` flag from the `zip_command` and `unzip_command`.  Note, you would also need to modify where these commands are used in their respective methods and remove the password parameter from being passed in the string.format().
