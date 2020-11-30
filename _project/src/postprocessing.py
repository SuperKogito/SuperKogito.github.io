import os
from bs4 import BeautifulSoup as Soup

def collect_file_paths(root_path):
    html_files = []
    # r=root, d=directories, f=files
    for r, d, f in os.walk(root_path):
        html_files += [os.path.join(r, file) for file in f if ".html" in file]
    return html_files

def read_html_file(html_file):
    with open(html_file, 'r') as f:
        html_code = f.readlines()
    return "".join(html_code)


def write_html_file(html_file, soup):
    with open(html_file, 'w') as f:
        f.write(str(soup))


def post_process(html_files):
    for html_file in html_files:

        try:
            print("Processing ", html_file)
            html_code = read_html_file(html_file)
            soup = Soup(html_code)
            title = soup.find('div', class_="section").h1

            metatag = soup.new_tag('meta')
            metatag.attrs['name'] = "viewport"
            metatag.attrs['content'] = "width=device-width, initial-scale=1.0"
            soup.head.append(metatag)

            # build menu html code
            menu = soup.new_tag("div", class_="sub-title-menu")
            path_to_file_in_html_folder = html_file.split("/html/")[1]
            prefix = "../" * (len(path_to_file_in_html_folder.split("/"))-1)

            # define menu code
            menu = f"""
             <div class="sub-title-menu">
             <table class="menu-table" id="menuTable" style="border:hidden;">
              <tr>
                <th>
                    <th>
                        <th class="icon"> <a href="{prefix}index.html"         title="Home"    ><i class="fa fa-home"        ></i></a> </th>
                        <th class="menu-label"> <a href="{prefix}index.html"         title="Home"    >Home</a> </th>
                    </th>
               </th>

                <th>
                    <th>
                        <th class="icon"><a href="{prefix}posts.html"         title="Posts"   ><i class="fa fa-bars"        ></i></a></th>
                        <th class="menu-label"><a href="{prefix}posts.html"         title="Posts"   >Posts</a></th>
                    </th>
               </th>

               <th>
                  <th>
                       <th class="icon"> <a href="{prefix}publications.html"  title="pubs"    ><i class="fa  fa-file-text"  ></i></a></th>
                       <th class="menu-label"> <a href="{prefix}publications.html"  title="pubs"    >Publications</a></th>
                    </th>
               </th>

                <th>
                    <th>
                        <th class="icon"> <a href="{prefix}projects.html"      title="projects"><i class="fa  fa-code"       ></i></a></th>
                        <th class="menu-label"> <a href="{prefix}projects.html"      title="projects">Projects</a></th>
                    </th>
                </th>

                <th>
                    <th>
                        <th class="icon"> <a href="{prefix}games.html"         title="Games"   ><i class="fa fa-gamepad"     ></i></a></th>
                        <th class="menu-label"> <a href="{prefix}games.html"         title="Games"   >Games</a></th>
                    </th>
               </th>

                <th>
                    <th>
                        <th class="icon"><a href="{prefix}about.html"         title="About"   ><i class="fa fa-user-circle" ></i></a></th>
                        <th class="menu-label"><a href="{prefix}about.html"         title="About"   >About</a></th>
                    </th>
               </th>

               <th>
                    <th>
                        <th class="icon"> <a href="#"                  onclick="modeSwitcher()"><i class="fa fa-adjust"      ></i></a></th>
                        <th class="menu-label"> <a href="#"                  onclick="modeSwitcher()"><text id="theme-toggle">DARK MODE</text></a></th>
                    </th>
               </th>
               </tr>
            </table>
            </div>
            """
            xa = """
                    <div class="sub-title-menu">
                      <a href="{prefix}index.html"         title="Home"    ><i class="fa fa-home"        ></i>Home</a>
                      <a href="{prefix}posts.html"         title="Posts"   ><i class="fa fa-bars"        ></i>Posts</a>
                      <a href="{prefix}publications.html"  title="pubs"    ><i class="fa  fa-file-text"  ></i>Publications</a>
                      <a href="{prefix}projects.html"      title="projects"><i class="fa  fa-code"       ></i>Projects</a>
                      <a href="{prefix}games.html"         title="Games"   ><i class="fa fa-gamepad"     ></i>Games</a>
                      <a href="{prefix}about.html"         title="About"   ><i class="fa fa-user-circle" ></i>About</a>
                      <a href="#"                  onclick="modeSwitcher()"><i class="fa fa-adjust"      ></i><text id="theme-toggle">DARK MODE</text></a>
                    </div>"""

            # insert menu code in page
            title.insert_after(Soup(menu))

            # add script
            footer =  soup.find('div', class_="footer")

            script          = f"""<script src="{prefix}_static/js/mode-switcher.js"></script>"""
            gh_script       = f"""<script async defer src="https://buttons.github.io/buttons.js"></script>"""
            chmod_converter = f"""<script src="{prefix}_static/js/chmod-converter.js"></script>"""
            jquerry         = f"""<script src="{prefix}_static/js/jquery.csv.min.js"></script><script src="{prefix}_static/js/jquery.csv.js"></script>"""
            d3_lib          = f"""<script src="http://d3js.org/d3.v3.min.js"></script>"""
            moment          = f"""<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/moment.min.js"></script>"""
            btc_visualizer  = f"""<script src="{prefix}_static/js/visualize-btc.js"></script>"""

            # debug: print(script)
            footer.insert_after(Soup(script))
            footer.insert_after(Soup(gh_script))

            if ("chmodmodes.html" in html_file or "chmod_converter.html" in html_file):
                footer.insert_after(Soup(chmod_converter))

            if ("btc_performance_heatmap_visualization.html" in html_file):
                footer.insert_after(Soup(jquerry))
                footer.insert_after(Soup(d3_lib))
                footer.insert_after(Soup(moment))
                footer.insert_after(Soup(btc_visualizer))

            # add meta img
            if "index.html" in html_file:
                metatag = soup.new_tag('meta')
                metatag.attrs['content'] = 'https://superkogito.github.io/_static/meta_ws_img.png'
                metatag.attrs['property'] = 'og:image'

                # define menu code
                soup.head.append(metatag)

            # overwrite file
            write_html_file(html_file, soup)

        except Exception as e:
            print(e, "while processing ", html_file)


if __name__ == "__main__":
    # get html files
    root_path = os.getcwd()[:-3]
    root_path = os.path.dirname(root_path) + "/docs/build/html"
    html_files = collect_file_paths(root_path)
    # post process
    post_process(html_files)
