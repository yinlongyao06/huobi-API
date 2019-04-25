
from HuobiServices import *

print(round(13.99999999, 2))
print("Account Information: ",get_accounts())

balance=get_balance()
print("Balance Information: ",balance)


pair=input('Please enter the symbol of the pair: ')
coin=input('Please enter name of coin: ')

margin_balance=margin_balance(pair)
print('margin balance information: ',margin_balance)

i=0
while True:
   if  margin_balance['data'][0]['list'][i]['currency']==coin and margin_balance['data'][0]['list'][i]['type']=='trade':
       coin_margin_avaliable_amount=float(margin_balance['data'][0]['list'][i]['balance'])
       break
   i=i+1

i=0
while True:
   if  margin_balance['data'][0]['list'][i]['currency']==coin and margin_balance['data'][0]['list'][i]['type']=='loan-available':
       coin_margin_loanable_amount_default=float(margin_balance['data'][0]['list'][i]['balance'])
       break
   i=i+1

i=0
while True:
   if  margin_balance['data'][0]['list'][i]['currency']==coin and margin_balance['data'][0]['list'][i]['type']=='loan':
       coin_margin_loaned_amount=-float(margin_balance['data'][0]['list'][i]['balance'])
       break
   i=i+1


i=0

print(coin,"margin available trade amount",coin_margin_avaliable_amount)
print(coin,"margin loaned amount",coin_margin_loaned_amount)

coin_lower_limit=float(input('Please input the lower limit of the coin: '))
coin_upper_limit=float(input('Please input the upper limit of the coin: '))
leverage_ratio=float(input('Please input the max leverage ratio of the coin: '))



coin_margin_loanable_amount=(coin_margin_loanable_amount_default+coin_margin_loaned_amount)/2*(leverage_ratio-1)

print(coin,"margin loanable amount",coin_margin_loanable_amount)

#如果账户钱不够，就借款
if coin_margin_avaliable_amount <= coin_lower_limit:
    coin_amount_needed_added=coin_lower_limit-coin_margin_avaliable_amount
    print('Please add',coin_amount_needed_added,' ',coin )
    #如果需要借的钱低于最高杠杆，可以借钱
    if coin_lower_limit < coin_margin_loanable_amount and round(coin_amount_needed_added,3)!=0.00 :
        coin_margin_add = get_margin(pair,coin, round(coin_amount_needed_added,3))
        print("Coin margin add: ",coin_margin_add)
    #否则，改变为0，无需操作
    elif round(coin_amount_needed_added,3)==0.00:
        print("No need to change your margin!")
    # 否则，无法借钱
    else:
        print('Cannot borrow more', coin, 'to satisfy your need!')

print('ok')


print('try loan orders')
loan_orders=loan_orders(pair,coin, start_date="", end_date="", start="", direct="next", size="")
print("Loan Orders: ",loan_orders)
print('try end')
order_list = list()
#loan orders length 是这样算的吗？
order_length = len(loan_orders['data'])
print('Order_length: ', order_length)


#如果借的钱太多了，可以还款
if coin_margin_avaliable_amount >= coin_upper_limit:
    #loan_orders=loan_orders(pair,coin, start_date="", end_date="", start="", direct="next", size="")
    print("Loan orders: ",loan_orders)
    coin_amount_needed_delete = coin_margin_avaliable_amount - coin_upper_limit
    print('Please sell', coin_amount_needed_delete, ' ', coin)
    #找到order list
    order_list=list()
    amount_list=list()
    order_length=len(loan_orders['data'])
    print('total order length of the pair: ', order_length)
    for i in range(order_length):
        if loan_orders['data'][i]['currency']==coin:
            order = loan_orders['data'][i]['id']
            amount = float(loan_orders['data'][i]["loan-balance"])
            order_list.append(order)
            amount_list.append(amount)

    coin_order_length=len(order_list)
    print('order length of the coin: ', coin_order_length)

    j=0
    while coin_amount_needed_delete > 0 and j < order_length:
        if coin_amount_needed_delete >= amount_list[j]:
            repay=repay_margin(order_list[j], amount_list[j])
            print('Repay: ',repay)
            coin_amount_needed_delete=coin_amount_needed_delete-amount_list[j]
            j=j+1
        else:
            repay = repay_margin(order_list[j], coin_amount_needed_delete)
            print('Repay: ', repay)
            coin_amount_needed_delete = 0
            j = j + 1
            break



#loan_orders=loan_orders(pair,coin, start_date="", end_date="", start="", direct="next", size="")
#print(loan_orders)
#coin_amount_needed_delete = coin_current_trade_amount - coin_upper_limit
#coin_amount_needed_delete = coin_upper_limit*11
#print('Please sell', coin_amount_needed_delete, ' ', coin)
#找到order list
#order_list=list()
#amount_list=list()
#order_length=len(loan_orders['data'])
#print('order_length', order_length)
#for i in range(order_length):
#    order=loan_orders['data'][i]['id']
#    amount=float(loan_orders['data'][i]["loan-balance"])
#    order_list.append(order)
#    amount_list.append(amount)

#j=0
#while coin_amount_needed_delete >= 0 and j < order_length:
#    if coin_amount_needed_delete >= amount_list[j]:
#        repay=repay_margin(order_list[j], amount_list[j])
#        print('repay',repay)
#        coin_amount_needed_delete=coin_amount_needed_delete-amount_list[j]
#        j=j+1
#    else:
#        repay = repay_margin(order_list[j], coin_amount_needed_delete)
#        print('repay', repay)
#        coin_amount_needed_delete = 0
#        j = j + 1
#        break