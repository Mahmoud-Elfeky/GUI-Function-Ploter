#import necessary modules and toolkit
from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

arithmatic_operations=[]
values_of_y=[]

#All Functions' Definations
def onKeyPress(event):
    """Get any pressed key , check it's charachter and add it's charachter to text box and arithmatic_operations list only if it valid
    Parameters
    ----------
    event : string
        The char of event / pressed key    
    Return
    -------
    'break'
        a strings returned if not valid charachter tying to be added/pressed 
    """
    if(input_box.get().strip()=='' and event.char in ['/','*','^']):        
        return 'break'
    elif( (not (event.char.isdigit()))  and  (event.char not in ['X','x','+','-','/','*','^','.'])):
        return 'break'
    elif(event.char in ['+','-','/','*','^']):                        
            insert_symbol(event.char)
            txt=input_box.get().strip()
            input_box.delete(0, 'end')
            input_box.insert('end',txt[:-1])
    elif(event.char=='.' and  input_box.get().strip()[-1]=='.'):
        return 'break'        

def validate_input(input_values):
    """apply validation process on the function's equation ,min value and max value and show sutabile massage based on condition
        check if any field is empty, all fields is accurae and all fields are acceptable

    Parameters
    ----------
    input_values : list of 3 item
        The values of the function's equation ,min value and max value

    Return
    -------
    bool
        a 0 bool returned if not valid case in input values , a 1 bool returned if all cases of input values is valid
    """    
    validation=1
    if('' in input_values):
        messagebox.showwarning("Empty Field", "Please fill all fields")        
        return 0
    
    if(input_box.get()[-1]in['+','-','/','*','^','.']):        
        messagebox.showerror("Invalid", "The function is not accurate")
        return 0
    try:        
        if(float(input_values[1]) > float(input_values[2])):
            messagebox.showerror("Error", "Min value must be less than Max value")            
            validation=0
    except:
        pass
    
    for each_char in input_values[0]:
        if not (each_char.isdigit()  or each_char in['X','x','+','-','/','*','^','.']):
            messagebox.showerror("Invalid", "function must contain numbers and arithematic symbols only")
            validation=0
    try:
        float(input_values[1])
    except:
        messagebox.showerror("Invalid", "min value must be numeric only")
        validation=0
    try:
        float(input_values[2])
    except:
        messagebox.showerror("Invalid", "max value must be numeric only")
        validation=0
            
    return validation

def split_input(input_equation):
    """Splitting function's equation into ready shape for calculations

    Parameters
    ----------
    input_equation : string 
        Contain the inputed function's equation 

    Return
    -------
    calc_list
        a list which contains 10 function's equation after prosessing (each item of the equation in a place alone on the same list)
    """
    calc_list=[]
    for i in input_equation:
            if i.isdigit():
                calc_list.append(i)
            elif i in ['+','-','/','*','^','.']:
                calc_list.append(i)
            elif i in ['x','X']:
                calc_list.append('x')
        
    for i in range(len(calc_list)):
        if calc_list[i].isdigit():
            c=1
            try:
                while(calc_list[i+c].isdigit() or  calc_list[i+c]=='.'):                    
                    calc_list[i]=calc_list[i]+calc_list[i+c]            
                    c+=1
            except:
                pass
            
            if not c==1:
                calc_list[i+1:c+i]='$'*(c-1)            
    return list(filter(('$').__ne__, calc_list))

def apply_calculation(symbol,operations,equ):
    """Apply sutable calculation's operation for a part of the equaction based on given symbol

    Parameters
    ----------
    symbol : string
        The charachter of the arithmatic calculation's operation 
    operations : list of operations such as[+,-,/,*,^] 
        operations which (remains/not applied) in inputed by user while inputed the function's equation
    equ : list 
        The items of the function's equation list    

    Return
    -------
    
    """
    index=(operations.index(symbol)*2)+1                    
    if(symbol=='^'):
        equ[index]=pow(float(equ[index-1]),float(equ[index+1]))
    elif(symbol=='*'):
        equ[index]=(float(equ[index-1])*float(equ[index+1]))
    elif(symbol=='/'):
        equ[index]=(float(equ[index-1])/float(equ[index+1]))
    elif(symbol=='+'):
        equ[index]=(float(equ[index-1])+float(equ[index+1]))
    elif(symbol=='-'):
        equ[index]=(float(equ[index-1])-float(equ[index+1]))
    equ.pop(index-1)
    equ.pop(index)
    operations.pop((index-1)/2)
   
def modify_and_evaluate(calc_list,x_values,operations1,values_of_y):
    """modify some items in the function's equation to be ready for calculations and then apply calculations based on actual mathematical concepts

    Parameters
    ----------
    input_values : list of 3 item
        The values of the function's equation ,min value and max value
    calc_list : list of 10 items
        10 modified equations identical to the inputed equation        
    x_values : list of 10 items
        10 values for x from min value to max value
    operations1 : list of operations such as[+,-,/,*,^] 
        operations which inputed by user while inputed the function's equation
    values_of_y : list of 10 items
        10 values for y after substituting by x_values in each equation of calc_list

    Return
    -------
    
    """
    equ=[]
    for iteration in range(0,10):
        for ind in range (len(calc_list)):
            if calc_list[ind] == 'x':                    
                equ.append(x_values[iteration])
            else:
                equ.append(calc_list[ind])
        operations=operations1[:]
        for operation in range(len(operations)):
            if '^' in operations:                
                apply_calculation('^',operations,equ)
            elif('*' in operations or '/' in operations):
                try:                                                                                
                    if operations.index('*') < operations.index('/'):
                        apply_calculation('*',operations,equ)
                    else:
                        apply_calculation('/',operations,equ)
                except:
                    if '*' in operations:
                        apply_calculation('*',operations,equ)
                    else:
                        apply_calculation('/',operations,equ)
            elif('+' in operations or '-' in operations):
                try:                                                                                
                    if operations.index('+') < operations.index('-'):
                        apply_calculation('+',operations,equ)
                    else:
                        apply_calculation('-',operations,equ)
                except:
                    if '+' in operations:
                        apply_calculation('+',operations,equ)
                    else:
                        apply_calculation('-',operations,equ)
                        
        print "equ",equ
        values_of_y.append(equ[0])
        print "values_of_y[:]",values_of_y
        equ=[]    
def processing_input():
    """invoke all above predefined functions to apply processing on inputed data and plot the shape of the equation at the end on the screen

    Parameters
    ----------
    
    Return
    -------
    
    """
    values_of_y=[]
    input_values_list= [input_box.get().strip(),min_box.get().strip(),max_box.get().strip()]
    
    if(validate_input(input_values_list)):

        #prepare supstituation values for given range
        range_values=[float(input_values_list[1])]
        common_value=(float(input_values_list[2])-float(input_values_list[1]))/10
        for index in range(0,8):            
            range_values.append(round(range_values[index]+common_value,2))
        range_values.append(float(input_values_list[2]))
        
        #split_input                
        calculations_list=split_input(input_values_list[0])
                                                        
        #modify_and_evaluate
        modify_and_evaluate(calculations_list,range_values,arithmatic_operations,values_of_y)
        
        #Start plotting 
        figure1 = plt.Figure(figsize=(5,6.5), dpi=100) # Create a figure , determine size    
        plot = figure1.add_subplot(1, 1, 1) # Define the points for plotting the figure
        plot.plot(range_values, values_of_y, color="red", linestyle="-",marker='.') # plot properties
        plot.set_title(input_box.get() + "  function's plot")
        # Add a canvas which contain would the figure ,show it and set it's place
        canvas = FigureCanvasTkAgg(figure1, screen)
        canvas.get_tk_widget().place(x=500,y=0)
    
def clear_equation_box():
    """clear the content of the function's box when clear button on the screen is pressed

    Parameters
    ----------

    Return
    -------
    
    """
    input_box.delete(0, 'end')
    arithmatic_operations[:]=[]    
    
def insert_symbol(s):
    """insert arithmatic symbol to the function's equation box if it agree with valid inputed cases in the program's logic
        else replace previous inputed arithmatic symbol or donothing then update arithmatic_operations list according to the condation

    Parameters
    ----------
    symbol : string
        The charachter of the arithmatic calculation's operation 

    Return
    -------
    
    """
    if(input_box.get().strip()=='' and (s=='+' or s=='-')):
        input_box.insert('end','0')
    elif(input_box.get().strip()==''):        
        return
    elif(input_box.get()[-1]in['+','-','/','*','^']):
        if(s in ['+','-','/','*','^']):
            arithmatic_operations[-1]=s        
        return
    
    arithmatic_operations.append(s)
    input_box.insert('end',s)    

#initializing window  and it's propertes       
screen=Tk()
screen.title('GUI')
screen.geometry('1000x650')
screen.resizable(False,False)
screen.configure(bg='gray10')
plot_frame=Frame(screen,width=500,height=650,bg='gray40')
plot_frame.place(x=500,y=0)

#program title label
program_name=Label(screen,text='Function Plotter',font=('Arial',35,'bold'),fg='blue3',bg='gray10')
program_name.place(x=70,y=50)

#function's equation label & box
function_label=Label(screen,text='Enter Function',font='Arail 15',fg='white',bg='gray10')
function_label.place(x=5,y=200)
input_box=Entry(screen,width=30,font='Arail 15',bg='gray',bd=3,justify=CENTER)
input_box.place(x=140,y=200)
input_box.bind('<KeyPress>', onKeyPress)

#min value label & box
min_label=Label(screen,text='min value',font='Arail 13',fg='white',bg='gray10')
min_label.place(x=220,y=350)
min_box=Entry(screen,width=6,font='Arail 15',bg='gray',bd=3,justify=CENTER)
min_box.place(x=300,y=350)

#max value label & box
max_label=Label(screen,text='max value',font='Arail 13',fg='white',bg='gray10')
max_label.place(x=220,y=400)
max_box=Entry(screen,width=6,font='Arail 15',bg='gray',bd=3,justify=CENTER)
max_box.place(x=300,y=400)

#equation's field clear button
add_btn=Button(screen,text="Clear",bg='white',fg='black',font='Arail 13 bold',bd=2,command=clear_equation_box)
add_btn.place(x=285,y=240)        

#equation's operations buttons
add_btn=Button(screen,text="+",bg='cyan4',fg='black',font='Arail 13 bold',bd=2,command=lambda :insert_symbol('+'))
add_btn.place(x=210,y=290)
sub_btn=Button(screen,text="-",bg='maroon',fg='black',font='Arail 13 bold',bd=2,command=lambda :insert_symbol('-'))
sub_btn.place(x=260,y=290)
mul_btn=Button(screen,text="*",bg='cyan4',fg='black',font='Arail 13 bold',bd=2,command=lambda :insert_symbol('*'))
mul_btn.place(x=310,y=290)
div_btn=Button(screen,text="/",bg='maroon',fg='black',font='Arail 13 bold',bd=2,command=lambda :insert_symbol('/'))
div_btn.place(x=360,y=290)
pow_btn=Button(screen,text="^",bg='cyan4',fg='black',font='Arail 13 bold',bd=2,command=lambda :insert_symbol('^'))
pow_btn.place(x=410,y=290)

#function's plot button
plot_btn=Button(screen,text="Plot",bg='deep sky blue3',fg='black',font='Arail 25',width=8,height=1,bd=4,command=processing_input)
plot_btn.place(x=220,y=480)

#start main window/screen
screen.mainloop()
