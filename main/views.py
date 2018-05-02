from django.http import HttpResponse


def index(request):
    return HttpResponse('<h1>Hey There</h1>')

def prices(request):
    return HttpResponse('''
    <table>
        <tr><td>Prices</tr>
            </td>Prices2</td>
        </tr>
    </table>''')
