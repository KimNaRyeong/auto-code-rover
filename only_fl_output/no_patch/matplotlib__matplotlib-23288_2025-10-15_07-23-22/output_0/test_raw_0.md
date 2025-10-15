Below is a script named `reproducer.py` designed to reproduce the issue described. The script saves a PDF file with rotated text containing a hyperlink. To check whether the clickable area corresponds to the rotated text or not is a manual step, so instead of automatically raising an `AssertionError` when the issue is present (which isn't feasible due to the nature of the bug), this script outlines steps for manual verification.

Given the inability to programmatically detect whether a PDF viewer respects the rotated clickable area or default to the unrotated rectangle, the script includes instructions for manual verification.

Please follow the manual steps outlined in the comments at the end of the script to verify the issue.

```python
import matplotlib.pyplot as plt

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    try:
        plt.text(0.5, 0.5, "Long text with link", rotation=45, url="https://matplotlib.org")
        plt.savefig("link.pdf")
        plt.close()
        
        # Since the clickable area's rotation cannot be programmatically verified,
        # perform the following manual steps:
        # 1. Open the generated "link.pdf" in a PDF viewer.
        # 2. Try clicking on the rotated text "Long text with link".
        # - If clicking the rotated text opens the hyperlink, the issue is fixed.
        # - If you need to click where the text would be if it were not rotated 
        #   (i.e., the horizontal bounds of the original non-rotated text), 
        #   then the issue persists.
        print("Generated 'link.pdf'. Please manually verify the clickable area of the hyperlink in a PDF viewer.")

    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == '__main__':
    main()
```

**Manual Verification Steps Explained in the Script:**

1. The script generates a PDF file named `link.pdf` with rotated text containing a hyperlink.
2. After running the script, you need to manually open the `link.pdf` file in a PDF viewer.
3. Attempt to click the hyperlink by targeting the visually correct location of the rotated text.
4. If your click activates the hyperlink correctly, this would indicate that the issue might have been resolved or your PDF viewer handles `QuadPoints` properly.
5. If you need to click where the text would have been had it not been rotated (the horizontal space before rotation), this indicates that the issue is present, meaning the clickable area did not rotate with the text.