from tkinter import *
from tkinter import messagebox
import requests
from PIL import ImageTk, Image

class Weather(Frame):
    def __init__(self, master):
        super(Weather, self).__init__(master)
        self.createWidgets()
        self.grid()

    def createWidgets(self):
        textLabel = Label(self, text = "Your city name:", font = ('Helvetica', 10))
        textLabel.grid(row = 1, column = 1, pady = 1, sticky="nsew")
        self.entryCity = Entry(self, width = 40, font = ('Helvetica', 10))
        self.entryCity.grid(row = 2, columnspan = 3, pady = 1, sticky="nsew")
        self.searchButton = Button(self, text = "Search", font = ('Helvetica', 10), command = self.search)
        self.searchButton.grid(row = 3, column = 1, pady = 5, sticky="nsew")
        self.resultName = Label(self, font = ('Helvetica', 20, 'bold'))
        self.resultName.grid(row = 4, columnspan = 3, pady = 0,sticky="nsew")
        self.resultCountry = Label(self, font=('Helvetica', 10, 'bold'))
        self.resultCountry.grid(row=5, columnspan=3, pady = 0, sticky="nsew")
        self.resultCondition = Label(self)
        self.resultCondition.grid(row=6, columnspan=3, pady=2, sticky="nsew")
        self.resultTemp = Label(self, font=('Helvetica', 20, 'bold'))
        self.resultTemp.grid(row=7, columnspan=3, pady=5,sticky="nsew")
        self.humidityImage = Label(self)
        self.humidityImage.grid(row=8, column=0, pady=1)
        self.pressureImage = Label(self)
        self.pressureImage.grid(row=8, column=1, pady=1)
        self.windImage = Label(self)
        self.windImage.grid(row=8, column=2, pady=1)
        self.resultHumidity = Label(self, font=('Helvetica', 10, 'bold'))
        self.resultHumidity.grid(row=9, column=0, pady=0, sticky="nsew")
        self.resultPressure = Label(self, font=('Helvetica', 10, 'bold'))
        self.resultPressure.grid(row=9, column=1, pady=0, sticky="nsew")
        self.resultWind = Label(self, font=('Helvetica', 10, 'bold'))
        self.resultWind.grid(row=9, column=2, pady=0, sticky="nsew")

    def getRequest(self):
        city = self.entryCity.get()
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=a0706d8057a5a1132be2ebbdc8da86ea&units=metric'.format(city)
        self.res = requests.get(url)

    def getData(self):
        self.getRequest()
        data = self.res.json()
        self.name = data['name']
        self.country = data['sys']['country']
        self.temp = data['main']['temp']
        self.humidity = data['main']['humidity']
        self.pressure = data['main']['pressure']
        self.wind = data['wind']['speed']
        self.weather = (data['weather'][0]['main']).lower()
        #print(self.weather)

    def images(self):
        self.humidityIcon = ImageTk.PhotoImage(Image.open('images\h.ico'))
        self.pressureIcon = ImageTk.PhotoImage(Image.open('images\p.ico'))
        self.windIcon = ImageTk.PhotoImage(Image.open('images\w.ico'))

        weatherDict = { 'snow': ImageTk.PhotoImage(Image.open('images\condition\w_snow.ico')),
                        'clear': ImageTk.PhotoImage(Image.open('images\condition\w_clear.ico')),
                        'rain': ImageTk.PhotoImage(Image.open('images\condition\w_rain.ico')),
                        'clouds': ImageTk.PhotoImage(Image.open('images\condition\w_clouds.ico')),
                        'thunderstorm': ImageTk.PhotoImage(Image.open('images\condition\w_thunder.ico')),
                        #'drizzle': ImageTk.PhotoImage(Image.open('images\w_drizzle.ico')),
                        'mist': ImageTk.PhotoImage(Image.open('images\condition\w_atmosphere.ico')),
                        'fog': ImageTk.PhotoImage(Image.open('images\condition\w_atmosphere.ico')),
                        'haze': ImageTk.PhotoImage(Image.open('images\condition\w_atmosphere.ico'))}

        self.conditionIcon = weatherDict.get(self.weather)

    def printData(self):
        self.getData()
        self.images()
        self.resultName['text'] = self.name
        self.resultCountry['text'] = self.country
        self.resultTemp['text'] = str(round(self.temp)) + ' \u2103'
        self.resultHumidity['text'] = str(self.humidity) + '%'
        self.resultPressure['text'] = str(self.pressure) + ' hpa'
        self.resultWind['text'] = str(self.wind) + ' m/s'

    def printImages(self):
        self.humidityImage['image'] = self.humidityIcon
        self.pressureImage['image'] = self.pressureIcon
        self.windImage['image'] = self.windIcon
        self.resultCondition['image'] = self.conditionIcon

    def search(self):
        self.getRequest()
        if self.res.status_code == 200:
            self.printData()
            self.printImages()
        else:
            messagebox.showerror("Error", "City was not found!")

root = Tk()
root.title("Weather App")
root.geometry("350x400")
root.wm_maxsize(350, 400)
root.wm_minsize(350, 400)
root.iconbitmap("fav.ico")
weather = Weather(root).pack()
root.mainloop()