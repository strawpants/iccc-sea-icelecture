# convenience tools for setting up lecture slides
# Roelof Rietbroek 2020

from IPython.display import Video,display_html,display_markdown,HTML,Markdown,display

import binascii

import os

import re

from lxml import etree as ET

from IPython.display import Markdown



def hideCode():   
    """Hides the code section of a jupyter notebook cell and only keep the output
    see also https://www.markroepke.me/posts/2019/06/05/tips-for-slideshows-in-jupyter.html"""

    uid = binascii.hexlify(os.urandom(8)).decode()
    html = """<div id="%s"></div>
    <script type="text/javascript">
        $(function(){
            var p = $("#%s");
            if (p.length==0) return;
            while (!p.hasClass("cell")) {
                p=p.parent();
                if (p.prop("tagName") =="body") return;
            }
            var cell = p;
            cell.find(".input").addClass("hide-in-slideshow")
        });
    </script>""" % (uid, uid)
    display_html(html, raw=True)



class FlexSlide():
    """Class which setups the cell output as a flex container, which allows more flexible structuring (see also the rise.css file)"""
    def __init__(self,title):
        hideCode()
        self.mdhead=title+"\n<div class=\"flxsld text_cell\" >\n"
        self.mdfoot="\n</div>"
        self.payload=""  

         

    def addimg(self,path,caption="",flxwidth=None,width=None,frag=False,alt=None):
        """Adds an image"""
        addcap=""
        cls=""
        if flxwidth:
            cls="class=\"%s\""%flxwidth
        if caption:
            addcap="<small>%s</small>"%caption
        if not alt:
            alt=caption

        if width:
            md="<div %s><img src=\"%s\" alt=\"%s\" style=\"width:%s;\" />%s</div>"%(cls,path,alt,width,addcap)
        else:
            md="<div %s><img src=\"%s\" alt=\"%s\" style=\"width:100%%;\"/>%s</div>"%(cls,path,alt,addcap)

        self.addmd(md,frag=frag)
            

    def addmd(self,mdcontent,frag=False,flxwidth=None):
        cls=""

        if flxwidth:
            cls+=flxwidth
        if frag:
            cls+=" fragment fade-in"

        self.payload+="\n<div class=\"%s\">\n\n"%(cls)+mdcontent+"</div>"


    def addVideo(self,path,width=None):
        self.addmd(Video(path)._repr_html_(),width=width)
        
    def addul(self,items,frag=False):
        """produces html ul item lists from item lists"""
        if type(items) != list:
            return ""

        html="<ul>"

        for item in items:
            if type(item) == list:
                #recursively call this function
                html+=self.addul(item,frag)
                continue

            if frag:
                html+="<li class=\"fragment fade-in\">%s</li>"%item
            else:
                html+="<li>%s</li>"%item

        html+="</ul>"
        return html

    def addItems(self,items,frag=False,flxwidth=None):       
        html=self.addul(items,frag)
        self.addmd(html,flxwidth=flxwidth)

    def addSVG(self,svgname,width=None,height=None):
        """Embed SVG as code in a code cell and fix relative links"""

        svgroot = ET.parse(svgname).getroot()
        if width:
            try:
                svgroot.attrib["width"]=width
                del svgroot.attrib["height"]
            except KeyError:
                pass
        elif height:
            try:
                svgroot.attrib["height"]=height
                del svgroot.attrib["width"]
            except KeyError:
                pass


        #change absolute embedded image links to relative links

        hrefky="{"+svgroot.nsmap["xlink"]+"}href"
        
        for el in svgroot.findall(".//{*}image[@"+hrefky+"]"):
            el.attrib[hrefky]=re.sub("\S+/images/","images/",el.attrib[hrefky])

        self.payload+="\n<div \">\n\n"+ET.tostring(svgroot).decode('utf-8')+"</div>"

    def addHTML(self,html):
        """adds pure html to a flexslide"""
        self.payload+="\n<div \">\n\n"+html+"</div>"

    def _repr_markdown_(self):
        # print("\n".join([self.mdhead,self.payload,self.mdfoot]))

        return "\n".join([self.mdhead,self.payload,self.mdfoot])

    
    def display(self):
        display(self)
