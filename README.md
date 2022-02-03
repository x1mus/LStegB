<h1 align="center">LStegB - LSB Image Steganography</h1>
The first time I discovered about LSB steganography implemented in image I thought it was a really cool way to hide informations in image without it being noticeable.
Then I documented myself to understand how it really works and how I could make my life easier when it come to this kind of challenge in CTF so I developped a brute-forcer !

## Description
This tool is made for people who wants to simplify their lives when encountering image steganography challenges during CTFs. It will always be under development (even if sometimes there's huge gaps).

New image format might blow up, some might disappear. The goal is to cover as much formats as possible to be (almost) sure you're not missing something about least significant bit steganography. Of course, this tool is not perfect. Some simple encoding pattern can easily defeat it.

Here's a trivial example :
- Using only prime numbers to choose which bits to hide information (this is not and will not be implemented in the bruteforcer)

## Installation
```bash
$ git clone https://github.com/MaxBresil/LStegB.git
$ cd LStegB
$ pip3 install -r requirements.txt
$ python3 LStegB.py -h
```

## Usage
To brute-force with all possible LSB methods **(-a/--all)**:
```bash
python3 LStegB.py -f FILE -a
```

To brute-force with the basic LSB method **(-b/--basic)**:
```bash
python3 LStegB.py -f FILE -b
```

To brute-force with the PIT method **(-i/--pit)**:
```bash
python3 LStegB.py -f FILE -i
```

## Contributing
Ways to contribute
- Suggest a feature
- Report a bug
- Fix something and open a pull request
- Help me document the code
- Spread the word

## Authors
I am the only writter of this tool. If you want to know a bit more about me, do not hesite to check out my other projects or even my [website](https://www.maximilien-laenen.be).

The list of people that contributed will be populated here as this project goes on.

## License
This project is under the MIT License - see the LICENSE.md file for details