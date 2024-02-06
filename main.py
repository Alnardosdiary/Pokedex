import flet as ft 
import aiohttp
import asyncio

#unica variable global
pokemon_actual = 0

#Funciones de la interfaz:
async def main(page:ft.Page):

   page.window_width= 720
   page.window_height=800
   page.window_resizable= False
   page.padding= 0
   page.fonts = {
      "zipx": "https://github.com/SolidZORO/zpix-pixel-font/releases/download/v3.1.8/zpix.ttf"
   }
   
   page.theme = ft.Theme(font_family= "zipx")
# Funciones para llamar a un pokemon: 
   async def peticiones_web(url):
      async with aiohttp.ClientSession() as sesion:
         async with sesion.get(url) as response:
            return await response.json()
  
   async def evento_pokemon(e: ft.ContainerTapEvent):
      global pokemon_actual
      if e.control == flecha_superior:
         pokemon_actual +=1
      else:
         pokemon_actual -=1

      numero= (pokemon_actual%150)+1
      resultado = await peticiones_web(f"https://pokeapi.co/api/v2/pokemon/{numero}")
      
      datos = f"Number:{numero}\nName: {resultado['name']}\n\nAbilities:"
      for elemento in resultado['abilities']:
            habilidad = elemento['ability']['name']
            datos += f"\n{habilidad}"
      datos += f"\n\nHeight: {resultado['height']}"
      texto.value = datos
      sprit_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{numero}.png"
      imagen.src = sprit_url
      await page.update_async()

#Brillo del boton azul: 
   async def Ice():
         while True:
            await asyncio.sleep(1)
            luz_azul.bgcolor = ft.colors.BLUE_200
            await page.update_async()
            await asyncio.sleep(0.1)
            luz_azul.bgcolor = ft.colors.BLUE
            await page.update_async()
# Interfaz:
   luz_azul = ft.Container(width=70, height=70, bgcolor=ft.colors.BLUE, left=5, top= 5, border_radius=50)
   boton_azul= ft.Stack([
      ft.Container(width=80, height=80, bgcolor=ft.colors.WHITE, border_radius=50),
      luz_azul,
   ])
#Fila superior:
   itens_superiores = [
      ft.Container(boton_azul, width=80, height=80),
      ft.Container(width=40, height=40, border=ft.border.all(), bgcolor=ft.colors.RED_200, border_radius=50),
      ft.Container(width=40, height=40, border=ft.border.all(), bgcolor=ft.colors.GREEN, border_radius=50),
      ft.Container(width=40, height=40, border=ft.border.all(), bgcolor=ft.colors.YELLOW, border_radius=50),
    ]
   sprit_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png"
   imagen = ft.Image(src= sprit_url,
        scale= 10,
        width= 30,
        height= 30,
        top=240/2,
        right=550/2
    )
#Fila central:
   Stack_central= ft.Stack([
      ft.Container(width=600, height=350, bgcolor=ft.colors.WHITE, border_radius=20),
      ft.Container(width=550, height=240, bgcolor=ft.colors.BLACK, left=25, top=25),
      imagen,
   ])
# Fila inferior: 
   triangulo = ft.canvas.Canvas([
        ft.canvas.Path(
                [
                    ft.canvas.Path.MoveTo(40, 0),
                    ft.canvas.Path.LineTo(0,50),
                    ft.canvas.Path.LineTo(80,50),
                ],
                paint=ft.Paint(
                    style=ft.PaintingStyle.FILL,
                ),
            ),
        ],
        width=80,
        height=50,
    )
   flecha_superior=ft.Container(triangulo, width=80, height=50, on_click=evento_pokemon)
   flechas = ft.Column(
      [
         flecha_superior,
         #radianes 180 = 3.14159
         ft.Container(triangulo, rotate=ft.Rotate(angle=3.14159), width=80, height=50, on_click=evento_pokemon) #flecha de disminucion
      ]
   )

   texto= ft.Text(
      value= "Esperando...",
      color=ft.colors.BLACK,
      size=20,
                  )
   
   itens_inferiores = [
      ft.Container(width= 50), #Margen izquierdo
      ft.Container(texto, padding=10, width=400, height=500, bgcolor=ft.colors.GREEN, border_radius=20),
      ft.Container(flechas, width=80, height=120),
      ft.Container(width=40), #Margen derecho
   ]

   superior = ft.Container(content= ft.Row(itens_superiores) ,height=80, width=600, margin=ft.margin.only(top=40))
   centro = ft.Container(content= Stack_central, height=280, width=600, margin=ft.margin.only(top=40),
                        alignment=ft.alignment.center)
   inferior = ft.Container(content= ft.Row(itens_inferiores), height=250, width=600, margin=ft.margin.only(top=40))

   colum = ft.Column(spacing=0, controls= [
      superior,
      centro,
      inferior,
   ])
   
   contenedor = ft.Container(colum, width=720, height=800, bgcolor= ft.colors.RED, alignment=ft.alignment.top_center)

   await page.add_async(contenedor)
   await Ice()
ft.app(target=main)