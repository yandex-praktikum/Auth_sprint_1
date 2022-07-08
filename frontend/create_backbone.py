#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 01.04.2021
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

import os, sys

snippet = '''.%s%s {
}
'''

res_snippet = '''
@media screen and (max-width: %spx) {
  .%s%s {
  }
}
'''

react_snippet = '''import React from 'react';

function %(comp)s(props) {
  return (
    <div className="%(comp)s">
    </div>
  );
}

export default %(comp)s;

'''

test_snippet = '''import { render, screen } from '@testing-library/react';
import %(comp)s from './%(comp)s';

test('renders %(comp)s component', () => {
  render(<%(comp)s />);
});
'''

### Settings section

root_folder = "src"

resolutions = [1280, 768, 320]

folders = [
    "components",
    "images",
    "pages",
    "contexts",
    "variables",
    "vendors",
    "utils",
    "vendors/fonts",
]

files = [
    ".nojekyll",
    "variables/variables.css",
    "pages/index.css",
    "vendors/normalize.css",
    "contexts/CurrentUserContext.js",
]

react_files = [
    "components/App.js",
    "components/Main.js",
    "components/Footer.js",
    "components/Header.js",
]

components = {
    "App": {

    },
    "Main": {

    },
    "Promo": {

    },
    "NavTab": {

    },
    "AboutProject": {

    },
    "Techs": {

    },
    "AboutMe": {

    },
    "Portfolio": {

    },
    "Movies": {

    },
    "SearchForm": {

    },
    "Preloader": {

    },
    "MoviesCardList": {

    },
    "MoviesCard": {

    },
    "SavedMovies": {

    },
    "Register": {

    },
    "Login": {

    },
    "Profile": {

    },
    "Bio": {

    },
    "Header": {

    },
    "Navigation": {

    },
    "Footer": {

    },
    "ErrorMessage": {

    },
    "ProtectedRoute": {

    },
    "ProgressBar": {

    },
    "Error404": {

    },

}

routers = [
    "/",
    "/movies",
    "/saved-movies",
    "/profile",
    "/signin",
    "/signup",
]

bem = {
    "page": {
      "e": ["__container", "__footer", "__header"],
      "m": [],
    },
    "header": {
      "e": ["__logo", "__lang-link"],
      "m": [("__lang-link", "_active", ""),],
    },
    "lead": {
      "e": ["__title", "__subtitle", "__image", "__figure", "__caption"],
      "m": [],
    },
    "intro": {
      "e": ["__title", "__text", "__list", "__list-text", "__list-number"],
      "m": [],
    },
    "photo-grid": {
      "e": ["__item"],
      "m": [],
    },
    "places": {
      "e": [],
      "m": [],
    },
    "place": {
      "e": ["__title", "__image", "__content", "__paragraph", "__website", "__url_heading", "__link"],
      "m": [],
    },
    "cover": {
      "e": ["__title", "__subtitle", "__link"],
      "m": [],
    },
    "footer": {
      "e": ["__link", "__copyright"],
      "m": [],
    },
}

### Backbone generation

for folder in folders:
    folder = os.path.join(root_folder, folder)
    if not os.path.isdir(folder):
        os.makedirs(folder)

for file_path in files:
    file_path = os.path.join(root_folder, file_path)
    if not os.path.isfile(file_path):
        with open(file_path, "w") as fw:
            content = ""
            fw.write(content)

index_page_css = os.path.join(root_folder, "pages", "index.css")

with open(index_page_css, "w") as fw_index:

    fw_index.write("@import url(../vendors/normalize.css);\n")
    fw_index.write("@import url(../vendors/fonts/inter.css);\n")
    fw_index.write("@import url(../variables/variables.css);\n")

    comp_root = os.path.join(root_folder, "components")
    for block in components:
        block_folder = os.path.join(comp_root, block)
        if not os.path.isdir(block_folder):
            os.makedirs(block_folder)
        file_path = os.path.join(block_folder, "%s.css" % block)
        if not os.path.isfile(file_path):
            with open(file_path, "w") as fw:
                content = snippet % (block, "")
                fw.write(content)
                for res in resolutions:
                    res_content = res_snippet % (res, block, "")
                    fw.write(res_content)
        file_path = os.path.join(block_folder, "%s.js" % block)
        if not os.path.isfile(file_path):
            with open(file_path, "w") as fw:
                content = react_snippet % {"comp": block}
                fw.write(content)
        file_path = os.path.join(block_folder, "%s.test.js" % block)
        if not os.path.isfile(file_path):
            with open(file_path, "w") as fw:
                content = test_snippet % {"comp": block}
                fw.write(content)
        fw_index.write("@import url(../components/%s/%s.css);\n" % (block, block))
            