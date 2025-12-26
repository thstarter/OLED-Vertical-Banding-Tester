# OLED-Vertical-Banding-Tester
A tool for exposing any vertical banding hiding in your OLED panel

#### Video Demo: https://www.youtube.com/watch?v=76sZr098TvU



#### Description

Welcome! OLED Vertical Banding Tester is a simple yet powerful tool that has been designed to help reveal vertical banding on your OLED panel to you by displaying pure grayscale backgrounds 
for your analysis. This program offers you the ability to cycle up to 255 possible grayscale backgrounds ranging from total white to total black and everything in between with intuitive controls at your fingertips. Along with grayscale testing, this program also gives you the ability to create an account and save grayscale presets for quick access and offers an information page that explores what vertical banding is and suggests steps the user can take to help reduce the amount of vertical banding the user finds.

What is vertical banding? Vertical banding is dark or light vertical lines that appear on OLED panels that become more visible under varying, uniform, grayscale backgrounds. It is often an undesirable effect that distracts the viewer from what they are viewing. Vertical banding on OLED panels however is unfortunately naturally inherent due to how OLED technology is designed. During the manufacturing of these OLED Panels, it is very difficult to maintain accurate and uniform pixel brightness in low light levels. Because the visual distraction of vertical banding is purely subjective, it is up to the user to determine if the degree and locations of the vertical banding falls within an acceptable range for them and is satisfactory enough to generally ignore. May all of your OLED panel's vertical banding align in your favor.



#### How it works

This program is built using Flask, SQLite3, Python, HTML, CSS, and Javascript. Flask handles routing, authentication, database interactions, and rendering templates. SQLite3 stores the user's credentials and saved grayscale presets. Python is used to code app.py. HTML is used to create the various files for the program. CSS is used to style the HTML files. Javascript is used in the tester file to give the user the ability to cycle grayscale values.



#### File overview

styles.css is a css styles sheet that will add color, font and border customizations to our program.

saves.db is our database that includes a table for the user's credentials and a table for the grayscale background settings that the user saved.

app.py is our main python file that will tie all of the files together and run the program as a whole. It contains Flask which will handle routing for all pages, authentication of the user's credentials, database interactions for saving grayscale presets and user credentials, and templates rendering. In other words, app.py runs the website and backend logic.

helpers.py contains python functions for our login and apology pages.

layout.html contains a navbar that is present through all of our html files. We are extending layout.html using jinja's {% extends %} syntax at the top of our html files.

apology.html is our html file that will display an error message and a picture to the user if the user submits invalid input with the program or performs an action that the program cannot process such as entering invalid user credentials on the register or login page.

home.html is our html file for the default home page for our program that acts a introductory/about page as well as a central hub containing all html pages that the user can navigate to.

info.html is our html file that simply displays information to educate the user on what vertical banding is and troubleshooting tips when it is spotted.

tester.html is our html file that is the main heart of this program and will allow the user to cycle through 255 possible grayscale backgrounds in order to search for vertical banding on their OLED panel. There will be a number of intuitive controls that the user can use including the arrow keys, - + keys, and the scroll wheel on the mouse. Users can save a grayscale background value by pressing both the ctrl and s key at the same time. 

register.html is our html file for the user to register their username and password.

login.html is our html file for the user to login using their newly created username and password which will also link them with the grayscale presets that the user saves.

saves.html is our html file that will display the grayscale background configurations that the user saved and allow them to quickly load a preset and jump straight to the corresponding grayscale background in the tester.html file. Users can also delete grayscale presets here as well. 





