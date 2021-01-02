"# Data_Scientist_Salary" 

https://towardsdatascience.com/selenium-tutorial-scraping-glassdoor-com-in-10-minutes-3d0915c6d905
https://chromedriver.chromium.org/downloads Chrome Driver 

pip install webdriver_manager --user 
pip install selenium

If you have anaconda:

Go to anaconda powershell, and right click run as administrator.
then type in this command:
conda install -c conda-forge selenium

After the installation, you can launch anaconda, and click on whichever IDE you're using. 
You should be able to import selenium. 




---- Only do this if you don't have anaconda 
Install selenium in the default settings: pip install selenium

Create virtual environment (on windows): py -m virtualenv folder_env

Activate virtual environment (on windows): source folder_env/Scripts/activate

Check virtual environment settings: which python and which pip

USE THIS FIRST, before you try to download it 
python -m pip install --upgrade pip

Install selenium: pip install selenium

Check pip list for selenium: pip list

(Optional) Exit virtual environment: deactivate folder_env
----------------------------------------------------------
For edit later:
When using the get_jobs functions make sure to make the delay based on your internet speed.

If you're getting an error such as (NEED TI BE FIX)
----
"StaleElementReferenceException: stale element reference: element is not attached to the page document
  (Session info: chrome=87.0.4280.88)"
Increase your delay to 30-50 if you have slow internet
----
ElementClickInterceptedException: element click intercepted: Element <div class="tab" data-test="tab" data-tab-type="rating" data-brandviews="MODULE:n=jobs-jobDescription:eid=20642:jlid=3782225961">...</div> is not clickable at point (883, 576). Other element would receive the click: <div id="JDCol" class="noPad">...</div>
  (Session info: chrome=87.0.4280.88)
---
ElementNotInteractableException: element not interactable: element has zero size
  (Session info: chrome=87.0.4280.88)

