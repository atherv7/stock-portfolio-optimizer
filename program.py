import numpy as np

def get_info():
    #getting the information from the user
    capital = input("Enter the amount of money you want to put in: ")
    number_of_stocks = input("How many stocks do you want to use: ")
    number_of_stocks = int(number_of_stocks)
    stock_paths = []
    i = 1
    while(i <= number_of_stocks):
        stock_paths.append(input("Enter the csv path of stock: "))
        i += 1
    
    #calculating all the expected returns for each of the stock
    expected_m_returns = []

    for path in stock_paths:
        expected_m_returns.append(calc_return(path))
    
    #to get the stock with the least amount of data
    least_days = len(expected_m_returns[0])-2

    for return_vals in expected_m_returns:
        least_days = min(least_days, len(return_vals)-2)

    #calculating the variances of all the stocks
    variances = []

    for return_vals in expected_m_returns:
        variances.append(return_vals[len(return_vals)-1] - (return_vals[len(return_vals)-2]))
    

    #calculating the covariances of all the stock pairs
    covariances = {}

    i = 0
    
    while(i < len(expected_m_returns)):
        j = i+1
        while(j < len(expected_m_returns)):
            key = str(i) + str(j)
            covariances[key] = calculate_cov(expected_m_returns[i], expected_m_returns[j], least_days)
            j += 1
        i += 1

    #filling the numpy matrix with the proper values 
    matrix = np.ndarray(shape=(number_of_stocks, number_of_stocks+1))

    i = 0
    while(i < number_of_stocks):
        j = 0
        while(j <= number_of_stocks):
            if(j == number_of_stocks):
                matrix[i,j] = 1
            elif(i != j):
                if(i < j):
                    key = str(i) + str(j)
                else:
                    key = str(j) + str(i)
                matrix[i, j] = covariances[key]
            else:
                matrix[i, j] = variances[i]
            j += 1
        i += 1
    
    #inserting the last row for the constraint function
    last_row = [1]*number_of_stocks
    last_row.append(0)

    matrix = np.vstack((matrix, last_row))

    #getting the solution vector
    vector = [0]*number_of_stocks
    vector.append(1)

    vector = np.array(vector)

    #solving the matrix equation
    solution = np.linalg.solve(matrix, vector)

    #checks if any of the solution is negative because then the user has to be notified to short 
    #the stocks 
    for vals in solution[:len(solution)]:
        if(vals < 0):
            print("You will have to short one of the stocks")
            return
    
    #displays the optimal distribution if the values are not negative
    for (ind, vals) in enumerate(solution[:len(solution)]):
        print("stock ", str(ind), ": ", str(vals*float(capital)))

    
    
    




#function to calculate the expected return (e[x]) and the expected squares of the returns (e[x^2])
def calc_return(stock_file):
    f_file = open(stock_file, "r")
    f_file.readline() 
    info = f_file.readlines() 
    count = 0
    sum_return = 0
    sum_sq_return = 0 
    ret = []
    #iterate through the csv file and subtract the opening price from the closing price to get the daily return
    #append it to the list that is going to be returned so those values can be used to calculate the covariance 
    #add the return to the sum_return and square the return and add it to the sum_sq_return, so we can calculate 
    #e[x]^2 and e[x^2] for variance
    for line in info: 
        line = line[:len(line)-1]
        parts = line.split(',')
        count += 1 
        close = float((parts[1])[1:])
        openi = float((parts[3])[1:])
        day_return = close - openi
        ret.append(day_return)
        sum_return += day_return
        sum_sq_return += (close - openi)**2
        count += 1
    
    #append e[x] value and e[x^2] value to the end of the list and then return the list
    ret.append(sum_return/count)
    ret.append(sum_sq_return/count)
    return ret


#calculate the covariance between the daily return of two stocks
def calculate_cov(arr_of_info_first, arr_of_info_second, days):
    #remove the e[x] and e[x^2] that is at the end of the list
    just_returns_first = arr_of_info_first[:len(arr_of_info_first)-2]
    just_returns_second = arr_of_info_second[:len(arr_of_info_second)-2]

    #get the expected return of the two stocks 
    expected_first = arr_of_info_first[len(arr_of_info_first)-2]
    expected_second = arr_of_info_second[len(arr_of_info_second)-2]

    sum = 0
    i = 0

    #calculating the sum at the top
    while(i < days):
        product = just_returns_first[i] - expected_first
        product *= just_returns_second[i] - expected_second
        sum += product
        i += 1
    
    #returning the covariance
    return (sum/days)

    
    

get_info()
