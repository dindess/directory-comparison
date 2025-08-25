# Directory Comparison with Jenkins Integration

This project provides a Python script for comparing directory structures and a Jenkins pipeline for automating Git repository comparisons.

---

## Components

### Python Script: "comparison5.py"
- **Functionality**
  - Accepts two directory paths as input.
  - Recursively compares:
    - Directory structures
    - File presence
    - File content
  - Generates a structured JSON report highlighting differences.
- **Output**
  - Identifies files present only in one repository.
  - Detects differences in content between files with the same name.
  - Includes folder paths for files that exist in only one directory. Example - "repo1" and "repo2" are variables depending on the input directories:

    {
      "only_in_repo1": [
        "requirements.txt"
      ],
      "only_in_repo2": [
        "Subfolder 1/subsubfolder2"
      ]
    }
    
  - Results are saved to "result_{timestamp}.txt".
    - The timestamp ensures uniqueness, traceability, and safe integration with downstream systems.

---

### 2. Jenkins Pipeline: `Jenkinsfile`
The pipeline automates repository comparison using the Python script. It is parameterized to accept:
- Two Git repository URLs
- Commits, branches, or tags for comparison

**Pipeline Stages**
1. **Checkout Comparison Script**  
   Retrieves the comparison script from its source repository.
2. **Clone Repositories**  
   Clones the two Git repositories specified as parameters.
3. **Run Comparison**  
   Executes the Python script and generates a timestamped result file.
4. **Publish Report**  
   Archives the result file as a Jenkins build artefact.
5. **Visualize Result**  
   Reads and displays the comparison output directly in the Jenkins console log.  
   Useful for quick checks during setup and troubleshooting without downloading the artefact.
6. **Upload to FTP**  
   Uploads the result artefact to a remote FTP server (credentials configured within the stage).

---

## Future Improvement Notes
- Error handling logic that points failures like failed clones, script errors, etc.;
- Enhanced output format - add beautified human-readable format, if needed;
- Mask sensitive data in the logs - credentials, for example;
- Automated job trigger when a repo change is detected;
- Artefact publish to other remote location options (S3/ssh).
