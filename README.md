<h1 align="center">LStegB - LSB Image Steganography</h1>
The first time I discovered about LSB steganography implemented in image I thought it was a really cool way to hide informations in image without it being noticeable.
Then I documented myself to understand how it really works and how I could make my life easier when it come to this kind of challenge in CTF so I developped a brute-forcer !

## Built with
Nothing else but my own hands !
I'm currently writing this program in Python 3 but one of my objective would be to translate this one in C to gain in performance.

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

To brute-force with the PVD method **(-v/--pvd)**:
```bash
python3 LStegB.py -f FILE -v
```

## Contributing
Ways to contribute
- Suggest a feature
- Report a bug
- Fix something and open a pull request
- Help me document the code
- Spread the word

## Versioning
I'm using [SourceTree](https://www.sourcetreeapp.com) for versioning.

## Authors
* **Laenen Maximilien** - *Developper of this tool*

## License
This project is licensed under the **MIT license** - see more information [HERE](https://github.com/MaxBresil/LStegB/blob/master/LICENSE)