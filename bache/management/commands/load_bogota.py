from django.core.management.base import BaseCommand
from bache.models import Localidad, UPZ, Barrio

DATOS_BOGOTA = {
    "USAQUEN": {
        "UPZs": {
            "Paseo de los Libertadores": ["Canaima", "La Floresta de La Sabana", "Torca"],
            "Verbenal": ["Altos de Serrezuela", "Balcones de Vista Hermosa", "Balmoral Norte", "Buenavista", "Chaparral", "El Codito", "El Refugio de San Antonio", "El Verbenal", "Horizontes", "La Estrellita", "La Frontera", "La Llanurita", "Los Consuelos", "Marantá", "Maturín", "Medellín", "Mirador del Norte", "Nuevo Horizonte", "San Antonio Norte", "Santandersito", "Tibabita", "Viña del Mar"],
            "La Uribe": ["Bosque de San Antonio", "Conjunto Camino del Palmar", "El Pite", "El Redil", "La Cita", "La Granja Norte", "La Uribe", "Los Naranjos", "San Juan Bosco", "Urbanización Los Laureles"],
            "San Cristóbal Norte": ["Ainsuca", "Altablanca", "Barrancas", "California", "Cerro Norte", "Danubio", "Don Bosco", "La Perla Oriental", "Las Areneras", "Milán (Barrancas)", "Pradera Norte", "San Cristóbal Norte", "San Cristóbal Norte parte alta", "San Cristóbal Norte parte baja", "Santa Teresa", "Soratama", "Torcoroma", "Villa Nydia", "Villa Oliva"],
            "Toberín": ["El Toberín", "Babilonia", "Darandelos", "Estrella del Norte","Guanoa", "Jardín Norte", "La Liberia", "La Pradera Norte", "Las Orquídeas", "Pantanito", "Santa Mónica", "Villa Magdala", "Villas de Aranjuez", "Villas del Mediterráneo", "Zaragoza"],
            "Los Cedros": ["Acacias", "Antigua", "Belmira","Bosque de Pinos", "Caobos Salazar", "Capri", "Cedritos", "Cedro Bolívar", "Cedro Golf", "Cedro Madeira", "Cedro Narváez", "Cedro Salazar", "El Contador", "El Rincón de Las Margaritas", "La Sonora", "Las Margaritas", "Lisboa, Los Cedros", "Los Cedros Oriental", "Montearroyo", "Nueva Autopista", "Nuevo Country", "Sierras del Moral el Nogal"],
            "Usaquén": ["Bella Suiza", "Bellavista", "Bosque Medina", "El Pañuelito","El Pedregal", "Escuela de Caballería I", "Escuela de Infantería", "Francisco Miranda", "Ginebra", "La Esperanza", "La Glorieta", "Las Delicias del Carmen", "Sagrado Corazón", "San Gabriel", "Santa Ana", "Santa Ana Occidental", "Santa Bárbara", "Santa Bárbara Alta", "Santa Bárbara Oriental", "Unicerros", "Usaquén"],
            "Country Club": ["Country Club", "La Calleja", "La Carolina"," La Cristalina", "Prados del Country", "Recodo del Country", "Santa Coloma", "Soatama", "Toledo", "Torres del Country", "Vergel del Country"],
            "Santa Bárbara": ["Santa Bárbara Occidental", "Campo Alegre", "Molinos del Norte", "Multicentro","Navarra", "Rincón del Chicó", "San Patricio", "Santa Bárbara", "Santa Bárbara Central", "Santa Bibiana", "Santa Paula"]
        }
    },
    "CHAPINERO": {
        "UPZs": {
            "El Refugio": ["Chicó Reservado", "Bellavista", "Chicó Alto", "El Nogal","El Refugio", "La Cabrera", "Los Rosales", "Seminario", "Toscana"],
            "San Isidro-Patios": ["La Esperanza Nororiental", "La Sureña", "San Isidro","San Luis Altos del Cabo"],
            "Pardo Rubio": ["Bosque", "Calderón", "Bosque Calderón Tejada","Chapinero Alto", "El Castillo", "El Paraíso", "Emaus", "Granada", "Ingemar", "Juan XXIII", "La Salle", "Las Acacias", "Los Olivos", "María Cristina", "Mariscal Sucre", "Nueva Granada", "Palomar", "Pardo Rubio", "San Martín de Porres", "Villa Anita", "Villa del Cerro"],
            "Chicó Lago": ["Antiguo Country", "Chicó Norte", "Chicó Norte II","Chicó Norte III", "Chicó Occidental", "El Chicó", "El Retiro", "Espartillal", "La Cabrera", "Lago Gaitán", "Porciúncula", "Quinta Camacho"],
            "Chapinero": ["Cataluña", "Chapinero Central", "Chapinero Norte","Marly", "Sucre"]
        }
    },
    "SANTA_FE": {
        "UPZs": {
            "Sagrado Corazón": ["La Merced", "Parque Central Bavaria", "Sagrado Corazón","San Diego", "Samper", "San Martín"],
            "La Macarena": ["Bosque Izquierdo", "Germania", "La Macarena","La Paz Centro", "La Perseverancia"],
            "Las Nieves": ["La Alameda", "La Capuchina", "Veracruz","Las Nieves", "San Victorino", "Santa Inés"],
            "Las Cruces": ["Las Cruces", "San Bernardo"],
            "Lourdes": ["Atanasio Girardot", "Cartagena", "El Balcón","El Consuelo", "El Dorado", "El Guavio", "El Mirador", "El Rocío", "El Triunfo", "Fábrica de Loza", "Gran Colombia", "La Peña", "Los Laches", "Lourdes", "Ramírez", "San Dionisio", "Santa Rosa de Lima", "Vitelma"]
        }
    },
    "SAN_CRISTOBAL": {
        "UPZs": {
            "San Blas": ["Aguas Claras", "Altos del Zipa", "Amapolas","Amapolas II", "Balcón de La Castaña", "Bella Vista Sector Lucero", "Bellavista Parte Baja", "Bellavista Sur", "Bosque de Los Alpes", "Buenavista Suroriental", "Camino Viejo San Cristóbal", "Cerros de San Vicente", "Ciudad de Londres", "Corinto", "El Balcón de La Castaña", "El Futuro", "El Ramajal", "El Ramajal (San Pedro)", "Gran Colombia (Molinos de Oriente)", "Horacio Orjuela", "La Castaña", "La Cecilia", "La Gran Colombia", "La Herradura", "La Joyita Centro (Bello Horizonte)","La Playa", "La Roca", "La Sagrada Familia", "Las Acacias", "Las Columnas", "Las Mercedes", "Laureles Sur Oriental II Sector", "Los Alpes", "Los Alpes Futuro", "Los Arrayanes Sector Santa Inés", "La Roca", "Los Laureles Sur Oriental I Sector", "Macarena Los Alpes", "Manantial", "Manila", "Miraflores", "Molinos de Oriente", "Montecarlo", "Nueva España", "Nueva España Parte Alta", "Ramajal", "Rincón de La Victoria-Bellavista", "Sagrada Familia", "San Blas", "San Blas (parcelas)", "San Blas II Sector", "San Cristóbal Alto", "San Cristóbal Viejo", "San Pedro Sur Oriental", "San Vicente", "San Vicente Alto", "San Vicente Bajo", " San Vicente Sur Oriental", "Santa Inés", "Santa Inés Sur", "Terrazas de Oriente", "Triángulo", "Triángulo Alto", "Triángulo Bajo", "Vereda Altos de San Blas", "Vitelma"],
            "Sociego": ["Golconda", "Primero de Mayo", "Buenos Aires","Calvo Sur", "La María", "Las Brisas", "Los Dos Leones", "Modelo Sur", "Nariño Sur", "Quinta Ramos", "República de Venezuela", "San Cristóbal Sur", "San Javier", "Santa Ana", "Santa Ana Sur", "Sosiego", "Velódromo", "Villa Albania", "Villa Javier"],
            "20 de Julio": ["Atenas", "20 de Julio", " Atenas I","Ayacucho", "Barcelona", "Barcelona Sur", "Barcelona Sur Oriental", "Bello Horizonte", "Bello Horizonte III Sector", "Córdoba", "El Ángulo", "El Encanto", "Granada Sur", "Granada Sur III Sector", "La Joyita", "La Serafina", "Managua", "Montebello", "San Isidro", "San Isidro I y II", "San Isidro Sur", "San Luis", "Sur América", "Villa de Los Alpes", "Villa de Los Alpes I","Villa Nataly", "20 de Julio"],
            "La Gloria": ["Altamira", "Altamira Chiquita", "Altos del Poblado","Altos del Virrey", "Altos del Zuque", "Bellavista Parte Alta", "El Pilar", "Bellavista Sur Oriental", "Buenos Aires", "Ciudadela Santa Rosa", "El Quindío", "El Recodo-República de Canadá", "El Rodeo", "La Colmena", "La Gloria", "La Gloria Baja", "La Gloria MZ 11", "La Gloria Occidental", "La Gloria Oriental", "La Gloria San Miguel", "La Grovana", "La Victoria", "La Victoria II Sector", "La Victoria III Sector", "Las Gaviotas","Las Guacamayas", "Las Guacamayas I", "Las Guacamayas II", "Las Guacamayas III", "Malvinas", "Miraflores", "Moralba", "Panorama", "Paseito III", "Puente Colorado", "Quindío", "Quindío I", "Quindío II", "San José", "San José Oriental", "San José Sur Oriental", "San Martín de Loba I", "San Martín de Loba II", "San Martín Sur", "San Miguel"],
            "Los Libertadores": ["Antioquia", "Canadá La Guirá", "Canadá La Guirá II Sector","Canadá-San Luis", "Chiguaza", "Ciudad de Londres", "El Paraíso", "El Pinar (República del Canadá II)", "El Triunfo", "Juan Rey (La Paz)", "La Belleza", "La Nueva Gloria", "La Nueva Gloria II Sector", "La Península", "La Sierra", "Los Libertadores", "Los Libertadores Sector El Tesoro", "Los Libertadores Sector La Colina", "Los Libertadores Sector San Ignacio", "Los Libertadores Sector San Isidro", "Los Libertadores Sector San José", "Los Libertadores Sector San Luis", "Los Libertadores Sector San Miguel", "Los Libertadores Bosque Diamante Triángulo", "Los Pinares","Los Pinos", "Los Puentes", "Nueva Delhi", "Nueva Gloria", "Nueva Roma", "Nuevas Malvinas (El Triunfo)", "República del Canadá", "República del Canadá-El Pinar", "San Jacinto", "San Manuel", "San Rafael Sur Oriental", "San Rafael Usme", "Santa Rita I", "Santa Rita II", "Santa Rita III", "Santa Rita Sur Oriental", "Valparaíso", "Villa Angélica-Canadá-La Guirá", "Villa Aurora", "Villa del Cerro", "Villabell", "Yomasa", "Villa Angélica", "El Paraíso Sur Oriental I Sector", "Juan Rey I", "Juan Rey II", "Villa Begonia"]
        }
    },
    "USME": {
        "UPZs": {
            "La Flora": ["Buenos Aires", "Costa Rica", "Doña Liliana","El Bosque km 11", "Juan José Rondón", "Juan José Rondón II Sector", "La Cabaña", "La Esperanza", "La Flora-Parcelación San Pedro", "Las Violetas", "Los Arrayanes", "Los Soches", "Tihuaque", "Unión", "Villa Diana", "Villa Rosita"],
            "Danubio": ["Alaska", "Arrayanes", "Danubio Azul","Daza Sector II", "Duitama", "El Porvenir", "El Porvenir II Sector", "Fiscala II La Fortuna", "Fiscala Sector Centro", "La Fiscala-Los Tres Laureles", "La Fiscala-Lote 16", "La Fiscala-Lote 16A", "La Fiscala Sector Daza", "La Fiscala Sector Norte", "La Fiscala Sector Rodríguez", "La Morena I", "La Morena II", "La Morena II (Sector Villa Sandra)", "Nueva Esperanza", "San Martín", "Villa Neiza", "Picota Sur", "Porvenir"],
            "Gran Yomasa": ["Almirante Padilla", "Altos del Pino", "Arizona","Barranquillita", "Benjamin Uribe", "Betania", "Betania II", "Bolonia", "Bulevar del Sur", "Casa Loma II", "Casa Rey", "Casaloma", "Compostela I", "Compostela II", "Compostela III", "El Bosque", "El Cortijo", "El Curubo", "El Jordán", "El Nevado", "El Pedregal", "El Recuerdo Sur", "El Refugio", "El Refugio Sector Santa Librada", "El Rosal-Mirador","El Rubí II Sector", "Gran Yomasa I", "Gran Yomasa II", "La Andrea", "La Aurora", "La Cabaña", "La Esperanza", "La Fortaleza", "La Regadera km 11", "La Regadera Sur", "Las Granjas de San Pedro (Santa Librada)", "Las Viviendas", "Los Tejares Sur II Sector", "Nuevo San Andrés de Los Altos", "Olivares", "Salazar Salazar", "San Andrés Alto", "San Felipe", "San Isidro Sur", "San Juan Bautista", "San Juan I", "San Juan II", "San Juan II y III", "San Luis", "San Pablo", "Santa Librada", "Santa Librada-La Esperanza", "Santa Librada-La Sureña", "Santa Librada-Los Tejares (Gran Yomasa)", "Santa Librada Norte", "Santa Librada-San Bernardino", "Santa Librada-San Francisco", "Santa Librada-Salazar Salazar", "Santa Librada Sector La Peña", "Santa Marta II", "Santa Martha", "Sierra Morena", "Tenerife II Sector", "Urbanización Costa Rica-San Andrés de los Altos", "Urbanización Brasilia II Sector", "Urbanización Brasilia Sur", "Urbanización Cartagena", "Urbanización La Andrea", "Urbanización La Aurora II", "Urbanización Miravalle", "Urbanización Tequendama", "Valles de Cafam", "Vianey", "Villa Alejandría", "Villa Nelly", "Villas de Santa Isabel (Parque Entrenubes)", "Villas del Edén", "Yomasita"],
            "Comuneros": ["Alfonso López Sector Charalá", "Antonio José de Sucre I", "Antonio José de Sucre II","Antonio José de Sucre III", "Bellavista Alta", "Bellavista II Sector", "Bosque El Limonar", "Bosque El Limonar II Sector", "Brazuelos Occidental", "Brazuelos-El Paraíso", "Brazuelos-La Esmeralda", "Centro Educativo San José", "Chapinerito", "Chicó Sur", "Chicó Sur II", "Ciudadela Cantarrana I Sector", "Ciudadela Cantarrana II Sector", "Ciudadela Cantarrana III Sector", "Comuneros", "El Brillante", "El Espino", "El Mortiño", "El Rubí", "El Tuno", "El Uval","El Virrey Última Etapa", "Finca La Esperanza", "La Esmeralda-El Recuerdo", "La Esperanza km. 10", "Las Brisas", "Las Flores", "Las Mercedes", "Lorenzo Alcantuz I", "Lorenzo Alcantuz II", "Los Altos del Brazuelo", "Marichuela III", "Monteblanco", "Montevídeo", "Nuevo San Luis", "San Joaquín-El Uval", "Sector Granjas de San Pedro", "Tenerife", "Urbanización Chuniza I", "Urbanización Jarón Monte Rubio", "Urbanización Líbano", "Urbanización Marichuela", "Usminia", "Villa Alemania", "Villa Alemania II Sector", "Villa Anita Sur", "Villa Israel", "Villa Israel II"],
            "Alfonso López": ["Alfonso López Sector Buenos Aires", "Alfonso López Sector El Progreso", "Brisas del Llano","El Nuevo Portal", "El Paraíso", "El Portal II Etapa", "El Progreso Usme", "El Refugio I y II", "El Triángulo", "El Uval II Sector", "La Huerta", "La Orquídea Usme", "La Reforma", "Nuevo Porvenir", "Nuevo Progreso-El Progreso II Sector", "Portal de La Vega", "Portal de Oriente", "Portal del Divino", "Puerta al Llano", "Puerta al Llano II", "Refugio I", "Villa Hermosa"],
            "Parque Entrenubes": ["Arrayanes", "Bolonia", "El Bosque Central","El Nuevo Portal II", "El Refugio I", "La Esperanza Sur", "Los Olivares", "Pepinitos", "Tocaimita Oriental", "Tocaimita Sur"],
            "Ciudad Usme": ["Ciudadela El Oasis", "Brisas del Llano", "Usme-Centro","El Bosque km 11", "El Pedregal-La Lira", "El Salteador", "La María"]
        }
    },
    "TUNJUELITO": {
        "UPZs": {
            "Venecia": ["Fátima", "Isla del Sol", "Laguneta","Nuevo Muzú", "Rincón de Muzú", "Rincón de Venecia", "Samore", "San Vicente Ferrer", "Tejar de Ontario","Venecia", "Ciudad Tunal", "El Carmen"],
            "Tunjuelito": ["Abraham Lincoln", "San Benito", "San Carlos","Tunjuelito"]
        }
    },
    "BOSA": {
        "UPZs": {
            "Apogeo": ["Jardines del Apogeo", "El Motorista", "Industrial","La Ilusión", "Nuevo Chile", "Olarte", "Villa del Río"],
            "Bosa Occidental": ["Amaru", "Berlín", "Berlín de Bosa","La Libertad III", "Betania", "Bosa Nova", "Bosa Nova II Sector", "Bosalinda (Holdebrando Olarte)", "Brasil", "Brasilia", "Campo Hermoso", "Casa Nueva", "Chicala", "Ciudadela La Libertad", "El Bosque de Bosa", "El Cauce", "El Diamante", "El Libertador", "El Paradero", "El Portal de La Libertad", "El Porvenir", "El Progreso", "El Recuerdo", "El Rincón de Bosa", "El Rodeo","El Sauce", "Escocia", "Finca La Esperanza", "Holanda", "Hortelanos de Escocia", "Jorge Uribe Botero", "La Concepción", "La Dulcinea", "La Esmeralda", "La Estanzuela I", "La Estanzuela II", "La Florida", "La Fontana de Bosa-La Libertad", "La Independencia", "La Libertad I", "La Libertad II", "La Libertad III", "La Libertad IV", "La Magnolia", "La María", "La Palma", "La Paz", "La Portada", "La Portadita", "La Veguita", "Las Margaritas", "Las Vegas", "Los Ocales", "Los Sauces", "Miami", "New Jersey", "Nuestra Señora de La Paz", "Nueva Escocia", "Nueva Esperanza", "Porvenir", "Potreritos", "San Antonio", "San Antonio de Bosa", "San Antonio de Escocia", "San Bernardino", "San Javier", "San Jorge", "San Juanito", "San Martín", "San Pedro", "Santa Inés", "Sauces", "Siracuza", "Tokio", "Vegas de Santana", "Villa Carolina", "Villa Clemencia", "Villa Colombia", "Villa de Los Comuneros", "Villa de Suaita", "Villa Magnolia", "Villa Natalia", "Villa Nohora", "Villa Sonia I", "Villa Sonia II", "Villas del Progreso", "Villas del Velero", "Campo Verde"],
            "Bosa Central": ["Andalucía I", "Andalucía II", "Antonia Santos","Argelia", "Bosa", "Bosques de Meryland", "Brasilia-La Estación", "Carlos Albán", "Charles de Gaulle", "Claretiano", "El Jardín, El Llano", "El Palmar", "El Portal de Bosa", "El Povenir", "El Progreso", "El Retazo", "El Toche", "Getsemaní", "Grancolombiano I", "Grancolombiano II", "Gualoche", "Hermanos Barragán", "Humberto Valencia", "Islandia", "Israelita"," Jiménez de Quesada", "José Antonio Galán", "José María Carbonel", "La Amistad", "La Azucena", "La Estación", "La Riviera", "Laureles", "Llano Oriental", "Llanos de Bosa", "Manzanares", "Mitrani", "Naranjos", "Nueva Granada", "Bosa Palestina", "Paso Ancho", "Piamonte", "Primavera Sur", "San Eugenio", "San Pablo I sector", "San Pablo II sector", "San Pedro", "Santa Lucía", "Urbanización Acuarela", "Betania", "Vereda San José", "La Esperanza", "Villa Anny", "Villa Bosa", "Villa Nohora", "Xochimilco"],
            "El Porvenir": ["Caldas", "Antonio Nariño", "Campo Hermoso","Cañaveralejo", "El Anhelo", "El Corzo", "El Porvenir", "El Recuerdo", "El Recuerdo de Santa Fe", "El Regalo", "La Arboleda", "La Cabaña", "La Granjita", "La Suerte", "La Unión", "Los Centauros", "Osorio X", "Osorio XIII", "Parcela El Porvenir", "San Bernardino II", "San Miguel", "Santa Fe I", "Santa Fe II", "Santa Fe III", "Santa Fe de Bosa","Villa Alegre", "Villa Alegría", "Villa Esmeralda", "Villa Karen"],
            "Tintal Sur": ["El Matorral", "El Matorral de San Bernardino", "El Triunfo","El Triunfo de San Bernardino", "La Vega de San Bernardino Bajo", "Potreritos", "San Bernardino Sector Potrerito", "San Bernardino XIX", "San Bernardino XVI", "San Bernardino XVII", "San Bernardino XVIII", "San Bernardino XXI", "San Bernardino XXV", "Ciudadela el Recreo"]
        }
    },
    "KENNEDY": {
        "UPZs": {
            "Castilla": ["Aloha Norte", "Agrupación de Vivienda Pio XII", "Andalucía I","Andalucía II", "Bavaria Techo II", "Bosques de Castilla", "Castilla La Nueva", "Castilla Los Mandriles", "Castilla Real", "Castilla Reservado", "Catania", "Catania-Castilla", "Ciudad Don Bosco", "Ciudad Favidi", "Ciudad Techo", "El Castillo", "El Condado", "El Portal de las Américas", "El Rincón de Castilla", "El Rincón de Los Ángeles", "El Tintal", "El Vergel", "Lagos de Castilla", "Las Dos Avenidas I y II Etapa", "Monterrey", "Multifamiliares El Ferrol", "Osorio", "Oviedo", "Pio XII", "San José Occidental", "Santa Catalina I", "Santa Catalina II", "Valladolid", "Villa Alsacia", "Villa Castilla", "Villa Galante", "Villa Liliana", "Villa Mariana", "Visión de Colombia"],
            "Américas": ["Agrupación Pío X", "Agrupación Multifamiliar Villa Emilia", "Alférez Real","Américas Central", "Américas Occidental I Etapa", "Américas Occidental II Etapa", "Américas Occidental III Etapa", "Antiguo Hipódromo de Techo II Etapa", "Banderas", "Carvajal II Sector", "Centroaméricas", "Ciudad Kennedy", "El Rincón de Mandalay", "Floresta Sur, Fundadores", "Glorieta de las Américas", "Hipotecho", "Igualdad I", "Igualdad II", "La Llanura", "Las Américas", "Los Sauces", "Mandalay", "Marsella III", "Nueva Marsella I", "Nueva Marsella II","Nueva Marsella III", "Provivienda Oriental", "Santa Rosa de Carvajal", "Villa Adriana", "Villa Claudia"],
            "Carvajal": ["Alquería de la Fragua", "Bombay", "Carimagua I","Carvajal", "Carvajal Osorio", "Carvajal Techo", "Condado El Rey", "Delicias", "Desarrollo Nueva York", "El Pencil", "El Progreso I", "El Progreso II", "El Triángulo", "Floralia I", "Floralia II", "Gerona", "Guadalupe", "La Chucua", "Las Torres", "Los Cristales", "Lucerna", "Milenta", "Nueva York", "Provivienda", "Provivienda Occidental","Salvador Allende", "San Andrés I", "San Andrés II", "Talavera de la Reina", "Tayrona Comercial", "Valencia-La Chucua", "Villa Nueva"],
            "Kennedy Central": ["Abraham Lincoln", "Casablanca I", "Casablanca II","Casablanca III", "Casablanca IV", "Casablanca 32", "Casablanca 33", "Ciudad Kennedy Central", "Ciudad Kennedy Norte", "Ciudad Kennedy Occidental", "Ciudad Kennedy Oriental", "Ciudad Kennedy Sur", "El Descanso", "La Giraldilla", "Miraflores Kennedy", "Multifamiliar Techo", "Nuevo Kennedy", "Pastrana", "Techo", "Puerto José de Caldas"],
            "Timiza": ["Alameda de Timiza", "Alfonso Montaña", "Berlín","Boitá I", "Boitá II", "Casa Loma", "Catalina", "Catalina II", "El Comité", "El Palenque", "El Porvenir", "El Rubí", "Jacqueline", "Juan Pablo I", "La Cecilia", "La Unidad", "Lago Timiza I Etapa", "Lago Timiza II Etapa", "Las Luces", "Moravia II", "Nuevo Timiza", "Onasis", "Pastrana", "Pastranita II", "Perpetuo Socorro","Prados de Kennedy", "Roma", "Roma II", "Sagrado Corazón", "San Martín de Porres", "Santa Catalina", "Timiza", "Tonoli", "Tocarema", "Tundama", "Vasconia II", "Villa de los Sauces", "Villa Rica"],
            "Tintal Norte": ["Santa Paz-Santa Elvira", "Vereda El Tintal", "Ciudad Tintal Ocidental"],
            "Calandaima": ["Urbanización Unir Uno (Predio Calandaima)", "Calandaima", " Conjunto Residencial Prados de castilla I"," Conjunto Residencial Prados de castilla II", " Conjunto Residencial Prados de castilla III", "Conjunto Residencial Gerona del Tintal", "Galán", "Osorio", "Santa Fe del Tintal", "Tintala", "Ciudadela Tierra Buena", "Ciudadela Primavera"],
            "Corabastos": ["Cayetano Cañizares", "Chucua de la Vaca", "El Amparo","El Llantito", "El Olivo", "El Saucedal", "La Concordia", "La Esperanza", "La María", "Llano Grande", "María Paz", "Pinar del Río", "San Carlos", "Villa de la Loma", "Villa de la Torre", "Villa Emilia", "Vista Hermosa"],
            "Gran Britalia": ["Alfonso López Michelsen", "Britalita", "Calarcá I","Calarcá II", "Casablanca Sur", "Class", "El Almenar", "El Carmelo", "Gran Britalia", "La Esperanza", "La María", "Pastranita", "Santa María de Kennedy", "Vegas de Santa Ana", "Villa Andrea", "Villa Anita", "Villa Nelly", "Villa Zarzamora", "Villas de Kennedy"],
            "Patio Bonito": ["Altamar", "Avenida Cundinamarca", "Barranquillita","Bellavista", "Campo Hermoso", "Ciudad de Cali", "Ciudad Galán", "Ciudad Granada", "Dindalito", "El Paraíso", "El Patio", "El Rosario", "El Saucedal", "El Triunfo", "Horizonte Occidente", "Jazmín Occidental", "La Rivera", "Las Acacias", "Las Brisas", "Las Palmeras", "Los Almendros", "Palmitas", "Patio Bonito I", "Patio Bonito II", "Patio Bonito III","Puente La Vega", "San Dionisio", "San Marino", "Santa Mónica", "Sumapaz", "Tayrona", "Tierra Buena", "Tintalito I", "Tintalito II", "Tocarema", "Villa Alexandra", "Villa Andrés", "Villa Hermosa", "Villa Mendoza"],
            "Las Margaritas": ["Las Margaritas", "Osorio XI", "Osorio XII","Portal Américas"],
            "Bavaria": ["Aloha", "Alsacia", "Áticos de las Américas","Cooperativa de Suboficiales", "El Condado de la Paz", "Los Pinos de Marsella", "Lusitania", "Marsella", "Nuestra Señora de La Paz", "San José Occidental", "Unidad Oviedo", "Urbanización Bavaria", "Ciudad Alsacia"]
        }
    },
    "FONTIBON": {
        "UPZs": {
            "Fontibón": ["Arabia", "Atahualpa", "Bahía Solano","Santiago Batavia", "Belén", "Betania", "Boston", "Centenario", "Centro A", "El Carmen", "El Cuco", "El Guadual", "El Jordan", "El Pedregal", "El Ruby", "El Tapete", "Ferrocaja", "Flandes", "Fontibón Centro", "La Cabaña", "La Giralda", "La Laguna", "Las Flores", "Palestina", "Rincón Santo","Santander", "Salamanca", "San Pedro-Los Robles", "Torcoroma", "Unidad Residencial Montecarlo", "Valle Verde", "Veracruz", "Versalles", "Villa Beatriz", "Villa Carmenza"],
            "Fontibón-San Pablo": ["Ambalema, Bohíos", "El Portal", "El Refugio","El Triángulo", "Florencia", "Jericó", "La Aldea", "La Estación", "La Perla", "La Zelfita", "Las Brisas", "Prados de la Alameda", "Puente Grande", "San Pablo", "Selva Dorada", "Villa Liliana", "Recodo"],
            "Zona Franca": ["Pueblo Nuevo", "Moravia", "Kasandra","Sabana Grande"],
            "Ciudad Salitre Occidente": ["Carlos Lleras", "La Esperanza Norte", "Salitre Nor-Occidental","Sauzalito"],
            "Granjas de Techo": ["El Franco", "Granjas de Techo", "Montevideo","Paraíso Bavaria", "Visión Semiindustrial"],
            "Modelia": ["Bosque de Modelia", "Baleares", "Capellanía","El Rincón de Modelia", "Fuentes del Dorado", "Hayuelos", "Cofradía", "La Felicidad", "La Esperanza", "Mallorca", "Modelia", "Modelia Occidental", "Santa Cecilia", "Tarragona"],
            "Capellanía": ["El Jardín", "La Rosita", "Puerta de Teja","San José", "Veracruz"],
            "Aeropuerto Eldorado": ["El Bogotano"]
        }
    },
    "ENGATIVA": {
        "UPZs": {
            "Las Ferias": ["Acapulco", "Bellavista", "Occidental","La Bonanza", "Bosque Popular", "Cataluña", "Ciudad de Honda", "El Dorado-San Joaquín", "El Guali", "El Laurel", "El Paseo", "Estrada", "La Cabaña", "La Estradita", "La Europa", "La Marcela", "Las Ferias", "Metrópolis", "Palo Blanco", "Santo Domingo"],
            "Minuto de Dios": ["Andalucía", "Ciudad Bachué", "Copetroco La Tropical","El Portal del Río", "La Palestina", "Tisquesusa", "La Española", "La Serena", "Los Cerezos", "Luis Carlos Galán", "Meissen-Sidauto", "Minuto de Dios", "Morisco", "París", "Gaitán", "Primavera Norte", "Quirigua"],
            "Boyacá Real": ["Boyacá", "El Carmelo", "El Refugio","Florencia", "Florida Blanca", "La Almería", "La Granja", "La Soledad Norte", "La Salina", "Los Pinos Florencia", "Maratu", "París", "Santa Helenita", "Santa María del Lago", "Santa Rosita", "Tabora", "Veracruz", "Zarzamora"],
            "Santa Cecilia": ["El Encanto", "El Lujan", "El Real","Los Monjes", "Normandía", "Normandía Occidental", "San Ignacio", "San Marcos", "Santa Cecilia", "Villa Luz"],
            "Bolivia": ["Bochica", "Bochica Compartir", "Bolivia","Ciudadela Colsubsidio", "El Cortijo"],
            "Garcés Navas": ["Garcés Navas", "Álamos", "Álamos Norte","Bosques de Mariana", "El Cedro", "Los Ángeles", "Molinos de Viento", "Plazuelas del Virrey", "San Basilio", "Santa Mónica", "Villa Amalia", "Villa Sagrario", "Villas de Granada", "Villas del Madrigal", "Villas del Dorado-San Antonio", "Bosques de Granada", "Parques de Granada", "Andalucía Parques de Granada", "Portal de Granada", "Rincón de Granada", "Granada Club Residencial", "La Rotana", "Mirador de los Cerezos"],
            "Engativá": ["Alameda", "Centauros del Danubio", "El Cedro","El Mirador", "El Muelle", "El Palmar", "El Triángulo", "El Verdún", "Engativá-Centro", "Granjas El Dorado", "La Cabaña", "La Esperanza", "La Faena", "La Riviera", "La Torquigua", "Santa Lucía Norte", "Las Mercedes", "Las Palmas", "Linterama", "Los Laureles", "Los Laureles-Sabanas El Dorado", "Marandú", "Porvenir", "Puerto Amor-Playas del Jaboque", "San Antonio Norte","San Basilio", "San José Obrero", "Santa Librada", "Villa Claver I", "Villa Claver II", "Villa Constanza", "Villas del Dorado Norte", "Villa Gladys", "Villa Mary", "Villa Sandra", "Villa Teresita", "Viña del Mar"],
            "Jardín Botánico": ["Luis María Fernández", "El Salitre"],
            "Álamos": ["San Ignacio", "Los alamos"]

        }
    },
    "SUBA": {
        "UPZs": {
            "La Academia": ["La Academia"],
            "Guaymaral": ["Guaymaral", "Conejera"],
            "San José de Bavaria": ["Gibraltar", "Guicani", "Mirandela","Nueva Zelandia", "Oikos", "San Felipe", "San José", "de Bavaria", "Santa Catalina", "Tejares del Norte", "Villanova", "Villa del Prado", "Villa Lucy"],
            "Britalia": ["Britalia", "Britalia San Diego", "Calima Norte","Cantagallo", "Cantalejo", "El Paraíso de los 12 Apóstoles", "Gilmar", "Granada Norte", "Granjas de Namur", "La Chocita", "Los Eliseos", "Pijao de Oro", "Portales del Norte", "San Cipriano", "Villa Delia", "Vista Bella"],
            "El Prado": ["Alcalá", "Atabanza", "Bernal","Forero", "Cacihia", "Canodromo", "La Sultana", "Libertadores", "Los Prados de La Sultana", "Madeira", "Manuela Arluz", "Mazurén", "Niza IX", "Prado Pinzón", "Prado Sur", "Prado Veraniego", "Prado Veraniego Norte", "Prado Veraniego Sur", "San José del Spring", "San José del Prado", "Santa Helena", "Tarragona", "Tierra Linda", "Victoria Norte", "Villa Morena"],
            "La Alhambra": ["Alhambra", "Batán", "El Recreo de los Frailes","Estoril", "Ilarco", "Malibú", "Mónaco", "Pasadena", "Puente Largo"],
            "Casablanca Suba": ["Atenas", "Catalayud", "Casa Blanca I","Casa Blanca II", "Casablanca Norte Suba", "Del Monte", "El Velero", "Escuela de Carabineros"],
            "Niza": ["Calatrava", "Campania", "Ciudad Jardín Norte","Colina Campestre", "Colinas de Suba", "Córdoba", "Covadonga", "Gratamira", "Iberia", "Lagos de Córdoba", "Las Villas", "Lindaraja", "Niza", "Niza Norte", "Niza Suba", "Niza VIII", "Prado Jardín", "Provenza", "Rincón de Iberia", "Sotileza"],
            "La Floresta": ["Andes Norte", "Club los Lagartos", "Coasmedas","Julio Flórez", "La Alborada", "La Floresta Norte", "Morato", "Nuevo Monterrey", "Pontevedra", "Potosí", "Santa Rosa", "San Nicolás", "Teusacá"],
            "Suba": ["Acacias", "Alaska", "Alcázar de Suba","Almendros Norte", "Alto de la Toma", "Bosques de San Jorge", "Campanela", "Costa Azul", "El Pencil", "Suba Compartir", "El Pinar", "Los Lagos", "El Pórtico", "El Salitre", "Java", "La Campiña", "La Fontana", "Gloria Lara", "Las Orquídeas", "Londres", "Miraflores", "Monarcas", "Navetas", "Prados de Suba", "Portal de Las Mercedes","Almendros de Suba", "Las Flores", "Pradera de Suba", "Prados de Suba", "Rincón de Santa Inés", "San Francisco", "Santa Isabel", "Suba Centro", "Tuna Alta", "Tuna Baja", "Turingia", "Vereda Suba Cerros", "Villa del Campo", "Villa Esperanza", "Villa Hermosa", "Villa Susana"],
            "El Rincón": ["Alcaparros", "Almirante Colón", "Almonacid","Altos de Chozica", "Altos de la Esperanza", "Amberes", "Antonio Granados", "Arrayanes, Aures I", "Arrayanes, Aures II", "Bochalema", "Catalina", "Ciudad Hunza", "Ciudadela Cafam", "Costa Azul", "Costa Rica", "El Aguinaldo", "El Arenal", "El Carmen", "El Cerezo", "El Cóndor", "El Jordan-La Esperanza", "El Poa", "El Naranjal", "El Ocal", "El Palmar","El Pórtico", "El Progreso", "El Refugio de Suba", "El Rubí", "El Tabor", "Gloria Lara de Echeverri", "Guillermo Núñez", "Jaime Bermeo", "Japón", "Java II Sector", "La Aguadita", "La Alameda", "La Aurora", "La Chucua", "La Esmeralda", "La Esperanza (Calle 131 A)", "La Estanzuela", "La Flor", "La Flora", "La Manuelita", "La Palma", "Lagos de Suba", "Las Flores", "Lombardía/comuneros", "Los Arrayanes", "Los Naranjos", "Los Nogales", "Naranjos Altos", "Palma Aldea", "Porterrillo", "Prados de Santa Bárbara", "Puerta del Sol", "Rincón de Suba", "Rincón El Cóndor", "Rincón-Escuela", "Riobamba", "Rodrigo Lara Bonilla", "San Cayetano", "San Isidro Norte", "San Jorge", "San Miguel", "San Pedro", "Santa Ana de Suba", "Taberín", "Telecom Arrayanes", "Teusaquillo de Suba", "Tibabuyes", "Trinitaria", "Villa Alexandra", "Villa Catalina", "Villa Elisa", "Villa María", "Villas del Rincón"],
            "Tibabuyes": ["Atenas", "Berlín", "Bilbao","Cañiza I", "Cañiza II", "Cañiza III", "Carolina II", "Carolina III", "El Cedro", "Compartir", "Fontanar del río", "La Gaitana", "La Isabela", "Lisboa", "Los Nogales de Tibabuyes", "Miramar", "Nueva Tibabuyes", "Nuevo Corinto", "Prados de Santa Bárbara", "Rincón de Boyacá", "Sabana de Tibabuyes", "San Carlos de Suba", "San Carlos de Tibabuyes", "San Pedro de Tibabuyes", "Santa Cecilia","Santa Rita", "Tibabuyes Universal", "Toscana", "Vereda Suba-Rincón", "Vereda Tibabuyes", "Verona", "Villa Cindy", "Villa de las Flores", "Villa Gloria"]


        }
    },
    "BARRIOS_UNIDOS": {
        "UPZs": {
            "Los Andes": ["Villa Calasanz", "Entre Ríos", "La Castellana","La Patria", "Los Andes", "Rionegro", "Urbanización San Martín", "Vizcaya"],
            "12 de Octubre": ["Doce de Octubre", "Jorge Eliécer Gaitán", "José Joaquín Vargas","La Libertad", "Rincón Del Salitre", "El Labrador", "Metrópolis", "Modelo Norte", "San Fernando", "San Miguel", "Simón Bolívar"],
            "Los Alcázares": ["1 de Noviembre", "Alcázares Norte", "Baquero","Benjamín Herrera", "Chapinero Noroccidental", "Colombia", "Concepción Norte", "Juan XXIII Norte", "La Aurora", "La Esperanza", "La Merced Norte", "La Paz", "Los Alcázares", "Muequetá", "Polo Club", "Quinta Mutis", "Rafael Uribe Uribe", "San Felipe", "Santa Sofía", "Siete de Agosto"],
            "Parque Salitre": ["El Rosario"]
        }
    },
    "TEUSAQUILLO": {
        "UPZs": {
            "Galerías": ["El Campín", "San Luis", "Chapinero Occidental","Galerías", "Banco Central", "Quesada", "Belalcázar", "Alfonso López Norte", "Palermo"],
            "Teusaquillo": ["La Soledad", "Santa teresita", "La Magdalena","Teusaquillo", "Las Américas", "La Estrella", "Armenia"],
            "Parque Simón Bolívar": ["Parque Metropolitano Simón Bolívar"],
            "La Esmeralda": ["Pablo VI", "Nicolás de Federmán", "Campin Occidental","Rafael Núñez", "La Esmeralda"],
            "Quinta Paredes": ["Acevedo Tejada", "El Recuerdo", "Gran América","Centro Nariño", "Quinta Paredes", "Ortezal"],
            "Ciudad Salitre Oriental": ["Ciudad Salitre Su-Oriental", "Ciudad Salitre Nor-Oriental"]
        }
    },
    "MARTIRES": {
        "UPZs": {
            "Santa Isabel": ["Eduardo Santos", "El Progreso", "El Vergel","Santa Isabel", "Veraguas"],
            "La Sabana": ["El Listón", "Estación de la Sabana", "La Estanzuela","La Favorita", "La Pepita", "Paloquemao", "Panamericano", "La Florida", "Ricaurte", "Samper Mendoza", "San Victorino", "Santa Fe", "Voto Nacional", "el Conjunto Residencial Usatama", "Unidad Residencial Colseguros", "la Unidad Residencial Sans Façon", "la Unidad Residencial Bulevar de Sans Façon", "La Favortia", "La estanzuela"]
        }
    },
    "ANTONIO_NARINO": {
        "UPZs": {
            "Ciudad Jardín": ["Policarpa", "Caracas", "Ciudad Berna","Ciudad Jardín", "Sevilla", "Luna Park", "La Hortúa"],
            "Restrepo": ["Restrepo", "Villa Mayor", "San Jorge Central","Cinco de Noviembre", "Eduardo Freí", "San Antonio", "La Fragua", "La Fraguita", "Santander"]
        }
    },
    "PUENTE_ARANDA": {
        "UPZs": {
            "Ciudad Montes": ["La Guaca", "Bochica", "Carabelas","Ciudad Montes", "El Sol", "Jazmín", "Jorge Gaitán Cortés", "Villa Inés", "La Asunción", "La Camelia", "Los Comuneros", "Ponderosa", "Primavera", "El Remanso", "San Eusebio", "Santa Matilde", "Tibaná", "Torremolinos"],
            "Muzú": ["Alcalá", "Alquería", "Autopista Sur","La Coruña", "Los Sauces", "Muzú", "Ospina Pérez", "Santa Rita", "Tejar", "Villa del Rosario", "Villa Sonia"],
            "San Rafael": ["Barcelona", "Bisas del Galán", "Camelia Sur","Colón", "Galán", "La Pradera", "La Trinidad", "El Arpay La Lira", "Milenta", "San Francísco", "San Gabriel", "San Rafael", "San Rafael Industrial", "Salazar Gómez"],
            "Zona Industrial": ["Cundinamarca", "El Ejido", "Gorgonzola","Industrial Centenario", "La Florida Occidental", "Los Ejidos", "Pensilvania"],
            "Puente Aranda": ["Batallón Caldas", "Centro Industrial", "Ortezal","Puente Aranda"]
        }
    },
    "LA_CANDELARIA": {
        "UPZs": {
            "La Candelaria": ["La Catedral", "La Concordia", "Las Aguas","Centro Administrativo", "Egipto", "Belén", "Nueva Santa Fe", "Santa Bárbara"]
        }
    },
    "RAFAEL_URIBE_URIBE": {
        "UPZs": {
            "San José": ["Bosque de San Carlos", "Country Sur", "Gustavo Restrepo","Pijaos", "San José Sur", "San Luis Sur", "Sosiego Sur"],
            "Quiroga": ["Claret", "Bravo Páez", "Centenario","Matatigres", "Murillo Toro", "Olaya", "Quiroga", "Santa Lucía", "Santiago Pérez", "El Inglés", "Villa Mayor Occidental"],
            "Marco Fidel Suárez": ["Colinas", "El Pesebre", "Granjas de San Pablo","Granjas de Santa Sofía", "Jorge Cavelier La Resurección", "Las Lomas", "Luis López de Mesa", "Marco Fidel Suárez", "Río de Janeiro El Pesebre", "San Jorge", "San Juanito", "San Justino", "Santa Lucia", "Olaya", "La Resureccion"],
            "Marruecos": ["Arboleda Sur", "Callejón Santa Bárbara", "Cerros de Oriente","Chircales", "Danubio Sur", "El Consuelo", "El Rosal", "El Socorro", "Gavaroba", "Guiparma", "La Merced del Sur", "La Picota Occidental", "La Playa", "Marruecos", "Mirador del Sur", "Molinos", "Nueva Pensilvania Sur", "Pradera Sur", "Puerto Rico", "Sarasota", "bochica", "Villa Gladys", "Villa Morales"],
            "Diana Turbay": ["San Agustín", "Diana Turbay", "El Portal", "La Esperanza Alta", "La Paz", "La Picota Oriental", " Palermo Sur ", "Palermo Sur - BRISAS", "Palermo Sur ( EL TRIANGULO)", "Palermo Sur LOS ARRAYANES", "Palermo Sur OSWALDO GOMEZ", "Palermo Sur SAN MARCOS", "Palermo Sur SANA FONSECA", "SAN AGUSTIN", "SAN AGUSTIN II SECTOR", "SERRANIA - SECTOR CULTIVOS"]
        }
    },
    "CIUDAD_BOLIVAR": {
        "UPZs": {
            "El Mochuelo": ["La Lira", "El Pedregal", "Villa Jacky","las Manas", "Mochuelo Oriental", "CENTRAL DE MEZCLAS"],
            "Monteblanco": ["El Mochuelo II", "Brazuelos de Santo Domingo", "Esmeralda","Lagunitas", "Paticos", "Barranquitos"],
            "Arborizadora": ["Arborizadora Baja", "Atlanta", "La Playa","Madelena", "Rafael Escamilla", "Santa Helena", "Santa Rosa Sur", "Villa Helena", "Casa linda", "La Coruña", "Protecho"],
            "San Francisco": ["San Francisco", "Las Acacias", "Candelaria La Nueva","Gibraltar", "Colmena", "La Casona", "Juan José Rondón", "San Luis Sur", "San Fernando Sur", "Santa Inés de la Acacia", "Millan Los Sauces", "Puerta del Llano", "Sauces", "Hortalizas", "El Recuerdo"],
            "Lucero": ["Álvaro Bernal Segura", "Lucero Alto", "Lucero Medio","Lucero Bajo", "Domingo Laín", "El Bosque", "El Castillo", "El Paraíso Mirador", "Bella Flor", "La Torre", "Estrella del Sur", "El Triunfo", "Gibraltar Sur", "Juan Pablo II", "La Alameda", "La Cabaña", "La Escala", "Las Manitas", "Los Alpes", "El Satélite", "La Torre", "Los Andes de Nutibara", "La Estrella de Lagos", "Ciudad Milagros", "Compartir","Buenavista", "Marandú", "Meissen", "Brisas del Volador", "México", "Nueva Colombia", "Naciones Unidas", "Tierra Linda", "Vista Hermosa", "Rincón del Diamante Villa Gloria", "VISTA HERMOSA SECTOR CAPRI", "VISTA HERMOSA SECTOR SAN CARLOS Y EL TRIANGULO", "URBANIZACION KALAMARY", "URBANIZACION LA ESCALA", "URBANIZACION LAS QUINTAS DEL SUR", "Vista Hermosa"],
            "El Tesoro": ["Arabia", "Acapulco", "Buenos Aires","Bogotá Sur", "Divino Niño", "Casa de Teja", "El Consuelo", "El Tesoro", "Tesorito", "El Mochuelo I", "El Reflejo", "La Cumbre", "Los Duques", "Inés Elvira", "Monterey", "Minuto de María", "Ocho de Diciembre", "Quiba", "Potreritos", "República de Venezuela", "República de Canadá", "San Rafael Sur", "San Joaquín del Vaticano", "Sotavento", "Villa Diana López"],
            "Ismael Perdomo": ["Bella Estancia", "Barlovento", "Caracolí","Bonanza Sur", "Casa Loma Casavianca", "Cerro del Diamante", "El Rosal", "El Espino", "Ismael Perdomo", "El Porvenir", "El Rincón del Porvenir", "Galicia", "La Carbonera", "Mirador de la Estancia", "Mirador de Primavera", "Perdomo Alto", "Rincón de Galicia", "Rincón de la estancia", "Rincón de la Valvanera", "San Antonio del Mirador", "San Isidro", "María Cano", "San rafael de la Estancia", "Santa Viviana", "Santo Domingo","Sierra Morena"],
            "Jerusalén": ["Arborizadora Alta", "Bella Vista", "Florida del Sur","Jerusalén", "La Pradera", "Las Brisas", "Potosí", "Las Vegas de Potosí", "Villas de Bolívar", "Verona", " VILLA CANDELARIA ANTES SAN SIMON I, II ETAPA", "URBANIZACION LA MILAGROSA"]
        }
    }
}


class Command(BaseCommand):
    help = 'Carga todas las localidades, UPZs y barrios de Bogotá'

    def handle(self, *args, **options):
        for localidad_nombre, data in DATOS_BOGOTA.items():
            localidad, _ = Localidad.objects.get_or_create(nombre=localidad_nombre)
            
            for upz_nombre, barrios in data["UPZs"].items():
                upz, _ = UPZ.objects.get_or_create(
                    localidad=localidad,
                    nombre=upz_nombre
                )
                
                for barrio_nombre in barrios:
                    Barrio.objects.get_or_create(
                        upz=upz,
                        nombre=barrio_nombre
                    )
        
        self.stdout.write(self.style.SUCCESS('¡Todos los datos de Bogotá se cargaron exitosamente!'))