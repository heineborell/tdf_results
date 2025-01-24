import getpass
from typing import Any, Dict, Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def start_driver(
    profile_number,
    disable_images: bool = True,
    detach: bool = True,
    disable_automation: bool = True,
    use_profile: bool = True,
    page_load_strategy: Optional[str] = None,
    additional_options: Optional[Dict[str, Any]] = None,
) -> webdriver.Chrome:
    """
    Initialize Chrome Driver with configurable options

    Args:
        disable_images: Whether to disable image loading
        detach: Keep browser open after script ends
        disable_automation: Hide automation flags
        use_profile: Whether to use a Chrome profile
        profile_number: Chrome profile number to use
        page_load_strategy: Strategy for page loading (normal/eager/none)
        additional_options: Dictionary of additional Chrome options to add

    Returns:
        Configured Chrome WebDriver instance
    """
    service = Service()
    options = Options()

    # Configure image loading
    if disable_images:
        options.add_argument("--blink-settings=imagesEnabled=false")

    # Configure browser detachment
    if detach:
        options.add_experimental_option("detach", True)

    # Configure automation flags
    if disable_automation:
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # Configure user profile
    if use_profile:
        username = getpass.getuser()

        options.add_argument(
            f"--user-data-dir=/Users/{username}/Library/Application Support/Google/Chrome/"
        )
        print(f"this is the profile number {profile_number}")
        options.add_argument(f"--profile-directory=Profile {profile_number}")

    # Configure page load strategy
    if page_load_strategy:
        options.page_load_strategy = page_load_strategy

    # Add any additional options
    if additional_options:
        for option_name, option_value in additional_options.items():
            if isinstance(option_value, bool):
                options.add_argument(f"--{option_name}")
            else:
                options.add_argument(f"--{option_name}={option_value}")

    return webdriver.Chrome(service=service, options=options)
