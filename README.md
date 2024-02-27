# A4P

## Autotune for People

A simple, free Autotune web app implemented in Flask &amp; Python.

Pitch correction effects are used to tune signals that are slightly out of key.\
Perhaps the most useful on vocal tracks, but can be used on anything!

**Online demo**:
[https://a4p.ezequielabregu.com/](https://a4p.ezequielabregu.com/)

&nbsp;
![Autotune for people in action](/static/autotune4people.gif)

## How to run

```bash
git clone https://github.com/ezequielabregu/Autotune4people.git
cd Autotune4people
pip install -r requirements.txt
python app.py
```

Then, open your web browser and navigate to [127.0.0.1:5000](http://127.0.0.1:5000/)

## Usage

Upload an audio file and select the key and mode for autotuning. The application will process the audio and provide a download link for the autotuned audio.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Folder permissions

Ensure that `forlder-permissions.sh` has execute permissions,

```bash
sudo chmod +x folder_permissions.sh
```

and execute the script

```bash
./folder_permissions.sh
```

## Caching

Numba (part of Librosa library) uses caching to improve the performance of your code by saving the compiled versions of your functions. This allows Numba to skip the compilation step when you run your code again, which can significantly speed up your code if you're running the same functions multiple times.

However, Numba does not automatically clean up its cache, which can lead to leftover in `cache` folder.

Delete the caching periodically is recommended:

`rm -rf cache/*`

## License

This project is licensed under the terms of the MIT license.