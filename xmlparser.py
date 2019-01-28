from xml.etree import ElementTree
import  os
import re
import csv

file_name = "movies.xml"
full_file = os.path.abspath(os.path.join('data', file_name))

try:
    parser = ElementTree.XMLParser(encoding="utf-8")
    dom = ElementTree.parse(full_file,parser=parser)

    tree = dom.getroot()

except ElementTree.ParseError as Error:
    print("Error while parsing xml file {}".format(Error))


def parse_xml(tree):
    """parses the xml file reads a perticular set of data 
    and store the data in dictionary and then append it to list.
    Also updates the xml files(creates new element under a perticular tag)
    """

    try:
        movi_list = list()
        movie_csv = list()
        for child in tree.findall("genre"):
            if child.attrib['category'] == "Action":
                main_dict = dict()
                for movies in child.findall('./decade/'):

                    movies_dict = {}
                    for movie in movies.findall('./'):

                        if movie.tag == "description":
                            text = movie.text.replace('\n', ' ').replace('\t', ' ')
                            text = re.sub('\s+', ' ', text)
                            movies_dict[movie.tag] = text
                        else:
                            movies_dict[movie.tag] = movie.text
                ## print("{} : {}".format(movie.tag,movie.text))
                ##print(movies_dict)
                    main_dict[movies.attrib['title']] = movies_dict
                    movi_list.append(main_dict)
                #  print(movie.tag,movie.text)

            elif child.attrib['category'] == 'Comedy':
                for movies in child.findall('./decade/'):

                    movie_dict2 = {}
                    for movie in movies.findall('./'):

                        if movie.tag == "description":
                            text = movie.text.replace('\n', ' ').replace('\t', ' ')
                            text = re.sub('\s+', ' ', text)
                            movie_dict2[movie.tag] = text
                        else:
                            movie_dict2[movie.tag] = movie.text

                    movie_csv.append(movie_dict2)

            elif child.attrib['category'] == 'Thriller':
                for movies in child.findall('./decade/'):
                    if movies.attrib['title'] == "American Psycho":
                        attrib = {}
                        element = movies.makeelement('actor', attrib)
                        movies.append(element)
                        element.text = "Christian Belle"

    except Exception as Error:
        print(Error)

    finally:
        dom.write('movies.xml')
        return movie_csv


def savetocsv(data):
    """saves the xml parsed data to the csvfile 
    using csv module
    """
    fields = ['format','year','rating','description']

    with open('movies.csv','w') as csvfile:

        writer = csv.DictWriter(csvfile,fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)

data = parse_xml(tree)
print(data)

res = savetocsv(data)

