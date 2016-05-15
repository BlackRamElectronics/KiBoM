import columns
from component import *
import os

BG_GEN = "#E6FFEE"
BG_KICAD = "#FFE6B3"
BG_USER = "#E6F9FF"
    
#return a background color for a given column title
def bgColor(col):
    #auto-generated columns
    if col == ColumnList.COL_GRP_QUANTITY:
        return BG_GEN
    #kicad protected columns
    elif col in ColumnList._COLUMNS_PROTECTED:
        return BG_KICAD
    #additional user columns
    else: 
        return BG_USER
    
def link(text):
    text = str(text)
    for t in ["http","https","ftp","www"]:
        if text.startswith(t):
            return '<a href="{t}">{t}</a>'.format(t=text)
            
    return text
    
"""
Write BoM out to a HTML file
filename = path to output file (must be a .htm or .html file)
groups = [list of ComponentGroup groups]
net = netlist object
headings = [list of headings to display in the BoM file]
prefs = BomPref object
"""

def WriteHTML(filename, groups, net, headings, prefs):
    
    if not filename.endswith(".html") and not filename.endswith(".htm"):
        print("{fn} is not a valid html file".format(fn=filename))
        return False
        
    with open(filename,"w") as html:
        
        #header
        html.write("<html>\n")
        html.write("<body>\n")
        
        #PCB info
        html.write("<h2>KiBoM PCB Bill of Materials</h2>\n")
        html.write('<table border="1">\n')
        html.write("<tr><td>Source File</td><td>{source}</td></tr>\n".format(source=net.getSource()))
        html.write("<tr><td>BoM Date</td><td>{date}</td></tr>\n".format(date=net.getDate()))
        html.write("<tr><td>Schematic Version</td><td>{version}</td></tr>\n".format(version=net.getVersion()))
        html.write("<tr><td>Schematic Date</td><td>{date}</td></tr>\n".format(date=net.getSheetDate()))
        html.write("<tr><td>KiCad Version</td><td>{version}</td></tr>\n".format(version=net.getTool()))
        html.write("<tr><td>Total Components</td><td>{n}</td></tr>\n".format(n = sum([g.getCount() for g in groups])))
        html.write("<tr><td>Component Groups</td><td>{n}</td></tr>\n".format(n=len(groups)))
        html.write("</table>\n")
        html.write("<br>\n")
        html.write("<h2>Component Groups</h2>\n")
        html.write('<p style="background-color: {bg}">Kicad Fields (default)</p>\n'.format(bg=BG_KICAD))
        html.write('<p style="background-color: {bg}">Generated Fields</p>\n'.format(bg=BG_GEN))
        html.write('<p style="background-color: {bg}">User Fields</p>\n'.format(bg=BG_USER))
        
        #component groups
        html.write('<table border="1">\n')
        
        #row titles:
        html.write("<tr>\n")
        if prefs.numberRows:
            html.write("\t<th></th>\n")
        for i,h in enumerate(headings):
            #cell background color
            bg = bgColor(h)
            html.write('\t<th align="center"{bg}>{h}</th>\n'.format(
                        h=h,
                        bg = ' bgcolor="{c}"'.format(c=bg) if bg else ''))
        html.write("</tr>\n")
        
        rowCount = 0
        
        for i,group in enumerate(groups):
        
            if prefs.ignoreDNF and not group.isFitted(): continue
            
            row = group.getRow(headings)
            
            rowCount += 1
            
                
            html.write("<tr>\n")
            
            if prefs.numberRows:
                html.write('\t<td align="center">{n}</td>'.format(n=rowCount))
                
            for n, r in enumerate(row):
                bg = bgColor(headings[n])
                
                html.write('\t<td align="center"{bg}>{val}</td>\n'.format(bg=' bgcolor={c}'.format(c=bg) if bg else '', val=link(r)))
                
        
            html.write("</tr>\n")
            
        html.write("</table>\n")
        html.write("<br><br>\n")
        
        html.write("</body></html>")
            
    return True