
# 🛠️ Building Corrupted Shadows from Source  
Last Updated for Release `v0.2.3-chapter1`

If you don't trust the pre-made `.exe` file or wish to compile it yourself, follow these instructions. This guide will teach you how to compile **Corrupted Shadows** into a standalone executable using **Python**, **Nuitka**, and **MSVC** (Microsoft Visual C++).

**Not interested in building from source?** Check out [Releases](https://github.com/Priestytheplushie/Priestys-Quest/releases) for pre-made `.exe` files and source code.

## ⚠️ Heads Up:  
This guide is for compiling for **Windows**. Other platforms may have a different process, and I only know how to compile for Windows. You should stick with the [pre-made](https://github.com/Priestytheplushie/Priestys-Quest/releases) `.exe` files unless you know what you are doing.

## Requirements  
Before attempting to compile, make sure you have **all** of the following:
- [Python](https://www.python.org/downloads/) 3.13 or later  
- [Pip](https://pypi.org/project/pip/) (Python package installer. Should be installed by Python)  
- [Microsoft Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) (MSVC)  
- Nuitka (For compiling the project. Instructions below)  
- [Git](https://git-scm.com/) (For cloning the Repository)

## Step 1: Clone the Repository  
Start by cloning the `Corrupted Shadows` Repository locally using [Git](https://git-scm.com/).

1. Make sure Git is installed  
2. Open a command prompt/terminal  
3. Clone the repository with the following command:

   ```bash
   git clone https://github.com/Priestytheplushie/Corrupted-Shadows.git
   ```
5. Navigate to the project directory:

   ```bash
   cd Corrupted-Shadows
   ```

## Step 2: Install Python  
If you don’t have Python installed, download and install it from the [official Python website](https://www.python.org/downloads/). Make sure to check the box that says **Add Python to PATH** during installation.  
To check if Python and pip are installed properly, open a second command prompt or terminal and run:

```bash
python --version
pip --version
```

## Step 3: Install Dependencies  
Navigate back to the project directory and use `pip` (Python package installer) to install the `requirements.txt`, which contains all the dependencies required. You can do this by running the following command in the **same** command prompt/terminal you used for Step 2 of the tutorial:

1. Navigate to the project directory:

   ```bash
   cd Corrupted-Shadows
   ```
3. Install dependencies from `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

## Step 4: Install Microsoft Visual C++ Build Tools (MSVC)  
To compile the game using Nuitka on Windows, you will need to install the MSVC Build Tools. Here's how to do it:

1. Download [Microsoft Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)  
2. Download and install the Build Tools for Visual Studio  
3. During the installation process, make sure to select the following components:
   - Desktop development with C++
   - MSVC v142 - VS 2019 C++ x64/x86 build tools
   - Windows 11 SDK  
4. After the installation is complete, restart your computer to ensure that the tools are properly set up  
5. To check if MSVC is installed correctly, follow these steps:  
6. Press `Start` and search for:  
  - "**x64 Native Tools Command Prompt for VS**" (for 64-bit builds), or  
  - "**Developer Command Prompt for Visual Studio**" 
7. Open it   
7. Run the following to check:
  ```
  cl
  ```

⚠️ If `cl` is not recognized in PowerShell or CMD, you’re likely not using the Developer Command Prompt. Go back and search for "x64 Native Tools Command Prompt for VS" and try again.

## Step 5: Install Nuitka  
Nuitka is a Python compiler that will convert the game to an executable (.exe) file for Windows. For more information on Nuitka, check out the [Nuitka Website](https://nuitka.net/).  
To install Nuitka, run the following command in your terminal or command prompt **that is in the project directory**:

```python
pip install nuitka
```
If you closed the terminal/command prompt from before, you can run the following to set a new terminal/command prompt to the project directory:

```bash
cd Corrupted-Shadows
```

## Step 6: Compile the Game  
Now that you've installed all dependencies and set up your build tools, it's time to compile the game into a Windows executable.

1. Make sure you are in the project directory. If you are not, use the following:

   ```bash
   cd Corrupted-Shadows
   ```
3. Compile the game using Nuitka. To build the game, use the following command:

   ```bash
   nuitka --standalone --onefile --msvc=latest main.py
   ```

**Flags:**  
- `--onefile`: Compiles everything into a single `.exe` file  
- `--standalone`: Ensures that all dependencies are bundled with the `.exe` file  
- `--msvc=latest`: Uses the previously installed MSVC (Microsoft Visual C++ Build Tools)  
- `main.py`: The root file which runs all the game code

3. Wait for the compilation to finish. Nuitka will start the compilation process, and once it's complete, the executable file will be generated in the `dist` directory.

## Step 7: Test the `.exe`  
Once the build process is complete, navigate to the `dist` directory and double-click the newly generated `.exe` file to run the game.  
Or use the following command in your terminal/command prompt to run the game instantly:

```bash
cd dist
./main.exe
```

## ✅ Done  
You now have your own compiled version of **Corrupted Shadows**. Now play the game and enjoy.

⚠️ **Note:** You'll need to repeat these steps in order to update your `.exe` to the next release.
