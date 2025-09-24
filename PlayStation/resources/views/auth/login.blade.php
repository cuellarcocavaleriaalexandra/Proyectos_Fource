<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PlayStation</title>
    <link rel="icon" href="{{ asset('images/PlayStation_logo.png') }}" type="image/png">
    @vite(['resources/css/app.css', 'resources/js/app.js'])
    <script src="https://cdn.tailwindcss.com"></script>
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
        }
        
        /* Capa semitransparente para mejorar legibilidad */
        main {
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 0.5rem;
        }
        
        /* Para el efecto de vidrio en el nav */
        .glass-nav {
            background: rgba(3, 68, 153, 0.8);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }
    </style>
</head>
<body class="bg-gray-100">
    <div class="min-h-screen flex items-center justify-center">
        <div class="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
            <img src="{{ asset('images/PlayStation_logo.png') }}" alt="PlayStation Logo" class="h-8 mr-2">
            <h1 class="text-2xl font-bold text-center mb-6">PlayStation</h1>
            
            @if(session('error'))
                <div class="mb-4 p-3 bg-red-100 text-red-700 rounded">
                    {{ session('error') }}
                </div>
            @endif
            
            <form method="POST" action="{{ route('login') }}">
                @csrf
                
                <div class="mb-4">
                    <label for="username" class="block text-gray-700 mb-2">Usuario</label>
                    <input type="text" id="username" name="username" 
                           class="w-full px-3 py-2 border rounded-lg @error('username') border-red-500 @enderror" 
                           value="{{ old('username') }}" required autofocus>
                    @error('username')
                        <span class="text-red-500 text-sm">{{ $message }}</span>
                    @enderror
                </div>
                
                <div class="mb-6">
                    <label for="password" class="block text-gray-700 mb-2">Contraseña</label>
                    <input type="password" id="password" name="password" 
                           class="w-full px-3 py-2 border rounded-lg @error('password') border-red-500 @enderror" 
                           required>
                    @error('password')
                        <span class="text-red-500 text-sm">{{ $message }}</span>
                    @enderror
                </div>
                
                <button type="submit" 
                        class="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition">
                    Iniciar Sesión
                </button>
            </form>
        </div>
    </div>
</body>
</html>