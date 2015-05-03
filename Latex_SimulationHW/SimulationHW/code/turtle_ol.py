import Tkinter
import turtle as tur



def forward( tur, d ):
    tur.fd( d )

def backward( tur, d ):
    tur.bk( d )

def neg_angle( tur, angle ):
    tur.left( angle )

def pos_angle( tur, angle ):
    tur.right( angle )

def push_state( tur, stack ):
    stack.append( tur.pos() )
    stack.append( tur.heading() )

def pop_state( tur, stack ):
    tur.setheading( stack.pop() )
    tur.penup()
    tur.setpos( stack.pop() )
    tur.pendown()

def interprit_line( tur, line, angle, distance, stack ):
    for x in line:
        if( x == 'F' ):
            forward( tur, distance )
        elif( x == 'G' ):
            forward( tur, distance )
        elif( x == '+' ):
            pos_angle( tur, angle )
        elif( x == '-' ):
            neg_angle( tur, angle )
        elif( x == '[' ):
            push_state( tur, stack )
        elif( x == ']' ):
            pop_state( tur, stack )


def main():
    file_name = "go"
    
    file_name = raw_input( 'Enter a file name or exit to quit program: ')
    while (file_name != "exit" and file_name != "Exit" and file_name != "quit" and file_name != "Quit"):

        f = open( file_name, 'r' )
    
        first_line = f.readline()
        first_line = first_line.split()
    
        distance = float( first_line[0] )
        angle = float( first_line[1] )
    
        stack = []

        wn = tur.Screen()

        for line in f:
            wn.clear()
            tur.penup()
            tur.seth(90)
            tur.setx(0)
            tur.sety(-200)
            tur.pendown()
            interprit_line(tur, line, angle, distance, stack)
        ts = tur.getscreen()
        ts.getcanvas().postscript(file=file_name +".eps")
        wn.exitonclick()

        file_name = raw_input( 'Enter a file name or exit to quit program: ')
if __name__ == "__main__":
        main()

