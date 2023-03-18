import pandas as pd
import matplotlib.pyplot as plt
import os

class GenerateChart():
    
    @staticmethod
    def get_stars_data(review_data):
        total_sum = {
            '5': 0,
            '4': 0,
            '3': 0,
            '2': 0,
            '1': 0
        }
        for item in review_data:
            star_amount = (item['stars_given'].replace(',', '.'))
            num = float(star_amount.split('/')[0])
            if num >= 4.5 and num <= 5.0:
                total_sum['5'] += 1
            elif num >= 3.5 and num < 4.5:
                total_sum['4'] += 1
            elif num >= 2.5 and num < 3.5:
                total_sum['3'] += 1
            elif num >= 1.5 and num < 2.5:
                total_sum['2'] += 1
            elif num >= 0.5 and num < 1.5:
                total_sum['1'] += 1
        return total_sum

    @staticmethod
    def get_recommendations_data(data):
        total_sum = {
            'recommended': 0,
            'not_recommended': 0,
            'no_recomendation': 0
        }
        for item in data:
            stripped = item['recommendation'].strip('\n')
            if stripped == "Polecam":
                total_sum['recommended'] += 1
            elif stripped == "Nie polecam":
                total_sum['not_recommended'] += 1
            else:
                total_sum['no_recomendation'] += 1
        return total_sum

    @staticmethod
    def generate_bar_chart(data, id):
        value_list = []
        for key in data.keys():
            value_list.append(data[key])
        df = pd.DataFrame({
            'Number of Stars': ['5', '4', '3', '2', '1'],
            'Amount of opinions': value_list
        })
        df.plot(x="Number of Stars", y=[
            'Amount of opinions'], kind="bar")
        
        dirname = os.path.dirname(__file__)
        new_dir = os.path.join(dirname, f"../charts_folder")
        plt.savefig(f'{new_dir}/bar-{id}.png')

    @staticmethod
    def generate_pie_chart(data, id):
        value_list = []
        for key in data.keys():
            value_list.append(data[key])
        df = pd.DataFrame({
            'Opinie': ['Polecam', 'Nie Polecam', 'Brak'],
            'Ilość': value_list
        })
        df.groupby(['Opinie']).sum().plot(
            kind='pie', y='Ilość')
        dirname = os.path.dirname(__file__)
        new_dir = os.path.join(dirname, f"../charts_folder")
        plt.savefig(f'{new_dir}/pie-{id}.png')