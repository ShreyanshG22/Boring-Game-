import cx_Freeze

executables = [cx_Freeze.Executable("game_increase_speed.py")]

cx_Freeze.setup(
    name="Boring Game!",
    version="1.0",
    description="Boring Game! is what you play when you are bored. So go have fun. Thank me later for making your life somewhat better...",
    author="ShreyanshG22",
    options={"build_exe": {"packages":["pygame", "math", "random"],
                           "include_files":["resources/"]}},
    executables = executables

    )
