from selenium import webdriver


def start_driver():
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
    options = webdriver.ChromeOptions()
    # options.page_load_strategy = "eager"
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    grid_url: str = "http://localhost:4444"
    return webdriver.Remote(command_executor=grid_url, options=options)
