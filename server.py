
from livereload import Server, shell




def main():
    server = Server()
    server.watch('templates/*.html', shell('python render_website.py'))
    server.serve(root='.', default_filename='pages/index1.html')


if __name__ == '__main__':
    main()
