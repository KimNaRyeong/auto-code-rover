 I apologize for the confusion. It seems that the issue is not reproducible in a standalone script. The issue may be related to the specific environment or configuration of your project.

To help diagnose the issue, you can try adding the following lines before the `plt.show()` call to print the version and backend information of Matplotlib:
```python
print(f"Matplotlib version: {matplotlib.__version__}")
print(f"Matplotlib backend: {plt.get_backend()}")
```
This will print the version and backend information to the console when the script is executed. You can then compare this information with the expected version and backend to see if there are any discrepancies.

If the issue is still not clear, you can try providing more context about the project and the environment in which the issue is occurring. This may include information about the dependencies, the version of Python, and any relevant configuration files.

I apologize for any inconvenience this may have caused.