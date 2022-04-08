use std::io;
use std::mem;
use std::mem::size_of;

struct mkmk {
    a : i32,
    b : f64,
    c : char,
    d : usize,
}

fn main() { /* */
    // let my_number: u8 = 100;
    // let my_other_number = 50;
    // let third_number = my_number + my_other_number;
    // println!("{}", third_number);
    // let mut guess = String::new();

    // io::stdin()
    // .read_line(&mut guess)
    // .expect("Fail to read line");

    println!("Size of a char: {} bytes", size_of::<char>());
    
    println!("Size of a mkmk: {} bytes", size_of::<mkmk>());

    let my_mkmk = mkmk
    {
        a : 1,
        b : 2.0,
        c : 'd',
        d : 1,
    };

    println!("{}", mem::size_of_val(&my_mkmk.b));
    println!("Size of string containing 'a': {}", "abc".len());

    //let my_vector = vec![1,2,3,4,5];

    //my_vector[2] = 11; // ERROR

    let mut my_vector2 = vec![1,3,5,7,9];

    my_vector2[2] = 11;

    //println!("{:?}", my_vector);
    println!("{:?}", my_vector2);
}
