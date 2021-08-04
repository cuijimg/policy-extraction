import bs4
import pandas as pd
import pathlib
import random
from dataclasses import dataclass
from flask import Flask, request, render_template, redirect, make_response
import json
import sys
sys.path.append('..')
import processor


policy_path = pathlib.Path("C:/Users/F-CUI/Desktop/ZEW/26")
ip = '10.1.141.117'


@dataclass
class Settings:
    name: str
    safe: bool


def replace_all_links(soup):
    """
    This function removes all tags that contain an external reference (so either a href or src attribute).
    For onw, this makes loading the page faster, especially if it was pulling data from the wayback machine.
    But since I don't know what the page would like to include, it is also safer.

    I also remove all scripts and delete all onload attributes.
    This will make the page look worse, but also better.

    :param soup: The bs4 element that I want stuff stripped from.
    :return: None, alterations are done in place.
    """
    for tag in soup.find_all(attrs={'src': True}):
        tag.replace_with_children()
    for tag in soup.find_all(attrs={'href': True}):
        tag.replace_with_children()

    for tag in soup.find_all('script'):
        tag.decompose()
    for tag in soup.find_all(attrs={'onload': True}):
        tag['onload'] = ''


class Policies:

    def __init__(self, csv_path: pathlib.Path):
        """
        Load a list of all csv files in the path.

        :param csv_path: The directory containing all csv input files to be processed.
        """
        self.csv_files = list(csv_path.glob("*.csv"))
        random.shuffle(self.csv_files)
        self.html = []

    def new_file(self) -> bool:
        """
        Load a new file from the path and extract the list of all websites.a

        :return: Are there more files to work on?
        """
        while len(self.html) <= 100:
            if len(self.csv_files) == 0:
                random.shuffle(self.html)
                return len(self.html) > 0
            # read in a new file and append it's content
            file = self.csv_files.pop()
            dat = pd.read_csv(file)
            # Get the unique policies
            for dig in dat.digest.unique():
                    ind = (dat.digest == dig).argmax()
                    tmp = dat.loc[ind, 'html']
                    if not pd.isna(tmp):
                        if str(tmp) == 'NaN':
                            print('NAN FOUND')
                            sys.exit(1)
                        self.html.append((f'{file.name.replace(".csv", "")}-{ind}', tmp))
        
        return True

    def next_result(self):
        """
        Processes one html website and returns the processed one.
        returns
        """
        
        # first load a new policy
        if len(self.html) == 0:
            if not self.new_file():
                return '', 'No more policies available'
        random.shuffle(self.html)
        id, html = self.html.pop()
        return id, processor.process(html)
    
    def next_result_same_firm(self):
        
        # first load a new policy
        if len(self.html) == 0:
            if not self.new_file():
                return '', 'No more policies available'
        id, html = self.html.pop()
        return id, processor.process(html)

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/login', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        # Get the settings and username and store them.
        new_setting = Settings(request.form['name'], request.form['safe'] == 'True')
        user_settings[new_setting.name] = new_setting
        response = make_response(redirect('/'))
        response.set_cookie('userID', new_setting.name)
        return response
    else:
        user = request.cookies.get('userID', None)
        if user is None or user not in user_settings:
            setting = None
        else:
            setting = user_settings[user]
        return render_template('login.html', name=setting.name if setting is not None else None)


@app.route('/', methods=['GET', 'POST'])
def view_patent():
    global decisions_counter
    global tmp_pol_dict
    # First get the user settings.
    cookie = request.cookies.get('userID', None)
    if cookie is None or cookie not in user_settings:
        return redirect('/login')
    setting = user_settings[cookie]

    if request.method == 'POST':
        form = request.form
        dat = {'id': user_policy_dict[cookie][0], 'user': setting.name,
               'isGood': form.get('isGood', ''), 'citation': form.get('cit', ''),
               'comment': form.get('text', '')}
        with open('decisions.json', 'a') as ofile:
            decisions_counter += 1
            ofile.write(json.dumps(dat) + '\n')

    id, policy = pol.next_result()
    user_policy_dict[cookie] = id, policy
    return render_template('policy.html', name=setting.name, id=id, counter=decisions_counter)

@app.route('/more', methods=['GET', 'POST'])
def view_patent_same():
    global decisions_counter
    global tmp_pol_dict
    # First get the user settings.
    cookie = request.cookies.get('userID', None)
    if cookie is None or cookie not in user_settings:
        return redirect('/login')
    setting = user_settings[cookie]

    if request.method == 'POST':
        form = request.form
        dat = {'id': user_policy_dict[cookie][0], 'user': setting.name,
               'isGood': form.get('isGood', ''), 'citation': form.get('cit', ''),
               'comment': form.get('text', '')}
        with open('decisions.json', 'a') as ofile:
            decisions_counter += 1
            ofile.write(json.dumps(dat) + '\n')

    id, policy = pol.next_result_same_firm()
    user_policy_dict[cookie] = id, policy
    return render_template('policy.html', name=setting.name, id=id, counter=decisions_counter)



@app.route('/policy')
def get_policy():
    # First get the user settings.
    user = request.cookies.get('userID', None)
    if user is None or user not in user_settings:
        return redirect('/login')
    setting = user_settings[user]

    policy = user_policy_dict[user][1]
    if setting.safe:
        if type(policy) is str:
            try:
                policy = bs4.BeautifulSoup(policy, 'lxml')
                replace_all_links(policy)
            except Exception as err:
                policy = f'Encountered {str(err)} while removing links'
    if policy is None:
        return "Error"
    return str(policy)


@app.route('/help')
def help_route():
    # First get the user settings.
    user = request.cookies.get('userID', None)
    if user is None or user not in user_settings:
        setting = None
    else:
        setting = user_settings[user]
    return render_template('help.html', name=setting.name if setting is not None else None)


user_policy_dict = {}
pol = Policies(policy_path)
user_settings = {}
if pathlib.Path('decisions.json').exists():
    with open('decisions.json') as ifile:
        for i, l in enumerate(ifile):
            pass
    decisions_counter = i + 1
else:
    decisions_counter = 0
if __name__ == '__main__':
    app.run(ip)