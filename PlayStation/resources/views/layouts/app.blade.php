<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>PlayStation</title>
    <!-- Favicon (imagen en el título) -->
    <link rel="icon" href="{{ asset('images/PlayStation_logo.png') }}" type="image/png">
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Configuración personalizada de Tailwind -->
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        'playstation-blue': '#00439C',
                        'playstation-blue-dark': '#00357a',
                        'playstation-blue-light': '#0052c3',
                        'playstation-accent': '#0072ce',
                    }
                }
            }
        }
    </script>
    <style>
        body {
            background-image: url("{{ asset('images/playstation_bg.png') }}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
            min-height: 100vh;
            padding-top: 64px; /* Altura del navbar */
        }
        
        /* Capa semitransparente para mejorar legibilidad */
        main {
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 0.5rem;
            margin-top: 1rem;
        }
        
        /* Para el efecto de vidrio en el nav */
        .glass-nav {
            background: rgba(3, 68, 153, 0.8);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 50;
        }
    </style>
</head>
<body class="text-gray-800">
    <nav class="glass-nav text-white p-4 shadow-lg">
        <div class="container mx-auto flex justify-between">
            <span class="flex items-center">
                <!-- Logo en el navbar -->
                <img src="{{ asset('images/PlayStation_logo.png') }}" alt="PlayStation Logo" class="h-8 mr-2">
                PlayStation
            </span>
            <form method="POST" action="{{ route('logout') }}">
                @csrf
                <button type="submit" class="hover:underline bg-playstation-blue-dark px-4 py-2 rounded hover:bg-playstation-accent transition-colors">
                    Cerrar sesión
                </button>
            </form>
        </div>
    </nav>

    <main class="p-6 container mx-auto">
        @yield('content')
    </main>
</body>
</html>