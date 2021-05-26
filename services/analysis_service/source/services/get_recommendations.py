from .service_base import ServiceBase


class GetRecommendations(ServiceBase):
    def __init__(self, portfolio):
        self.portfolio = portfolio

    async def execute(self):
        return recommend(self.portfolio)


def recommend(df, available_price):
    start_price = available_price
    
    df['price'] = df['price'].apply(lambda x: float(x.replace(',', '.')))
    df['price_all'] = df['price'] * df['count']
    diagram_df = df.groupby('sector')['price_all'].sum().reset_index()
    diagram_df['persent'] = diagram_df['price_all'].apply(
        lambda x: format((x / diagram_df['price_all'].sum()) * 100, '.2f'))
    spheres = ['Other', 'HealthCare', 'IT', 'Industrials', 'RealEstate', 'Consumer', 'Materials',
               'Telecom', 'Financial', 'Utilities', 'Energy']
    price = []
    percent = []
    for sfer in spheres:
        if sfer in list(diagram_df['sector']):
            price.append(float(diagram_df[diagram_df['sector'] == sfer]['price_all']))
            percent.append(float(diagram_df[diagram_df['sector'] == sfer]['persent']))
        else:
            price.append(0.0)
            percent.append(0.0)
    diagram = {'sector': spheres,
               'price': price,
               'percent': percent}
    #print(diagram)
    available_spheres = []
    available_percent = []
    for i in range(len(spheres)):
        if percent[i] < 30:
            available_spheres.append(spheres[i])
            available_percent.append(percent[i])
    available_df = pd.DataFrame({'available_spheres':available_spheres,'available_percent':available_percent})
    available_df = available_df.sort_values(by='available_percent')
    available_spheres = available_df['available_spheres']
    #print(available_spheres)
    good_stock = pd.read_csv('good_stock.csv',sep='\t')
    
    tiker = []
    name = []
    price = []
    
    for available_spher in available_spheres:
        for i in range(len(good_stock[good_stock['sector']==available_spher])):
            #print(str(i)+'___'+available_spher)
            price_ = float(good_stock[good_stock['sector']==available_spher].sort_values(by='capitalization', ascending=False).iloc[i]['price'].replace(',','.'))
            
            if price_ <=available_price:
                #print(good_stock[good_stock['sector']==available_spher].sort_values(by='capitalization', ascending=False).iloc[i]['tikers'])
                tiker.append(good_stock[good_stock['sector']==available_spher].sort_values(by='capitalization', ascending=False).iloc[i]['tikers'])
                name.append(good_stock[good_stock['sector']==available_spher].sort_values(by='capitalization', ascending=False).iloc[i]['names'])
                price.append(price_)
                break
    #print(tiker)
    recommendations = []
    
    tiker_for_buy = []
    name_for_buy = []
    price_for_buy = []
    amount_for_buy = []
    total_for_buy = []
    
    check = 1
    while check != 0:
        check = 0
        for i in range(len(tiker)):
            if available_price - price[i] >=0:
                if tiker[i] not in tiker_for_buy:
                    tiker_for_buy.append(tiker[i])
                    name_for_buy.append(name[i])
                    price_for_buy.append(price[i])
                    amount_for_buy.append(1)
                    check = 1
                else:
                    index = tiker_for_buy.index(tiker[i])
                    amount_for_buy[index] += 1
                    check = 1
                available_price = available_price - price[i]
    #print(tiker_for_buy)
    for i in range(len(tiker_for_buy)):
        total_for_buy.append(price_for_buy[i] * amount_for_buy[i])
        
    for i in range(len(tiker_for_buy)):
        recommendations.append(
        {
            'tiker': tiker_for_buy[i],
            'name' : name_for_buy[i],
            'price': price_for_buy[i],
            'amount': amount_for_buy[i],
            'total': round(total_for_buy[i], 2)
        }
        )
    sum_end = round(start_price - available_price, 2)
    
    return {'recommendations':recommendations, 'sum':sum_end}

def add_cost_sector(portfolio):
    user_json = portfolio
    names = []
    count = []
    for i in range(len(user_json['stocks'])):
        names.append(user_json['stocks'][i]['name'])
        count.append(user_json['stocks'][i]['amount'])
    df_user = pd.DataFrame({'names': names, 'count': count})
    df = pd.read_csv('stock.csv',sep='\t')
    full_df = df_user.merge(df)
    return full_df


def main():
    # df_all = parse_stock ()
    # print(len(df_all))
    user_json = {'stocks': [
        {'name': 'MD Medical Group Investments PLC',
         'amount': 1},
        {
            'name': 'Globaltrans Investment PLC',
            'amount': 2},
        {
            'name': 'Транснефть',
            'amount': 3}
    ]}
    df = add_cost_sector(user_json)
    available_price = 10000
    final_df = recommend(df, available_price)
    print(final_df)


if __name__ == "__main__":
    main()
