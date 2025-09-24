<nav class="bg-white shadow">
    <div class="container mx-auto px-4 py-3 flex justify-between items-center">
        <a href="/" class="text-xl font-bold text-gray-800">PlayStation DB</a>
        
        @auth
        <div class="flex items-center space-x-4">
            <span class="text-gray-600">Hola, {{ Auth::user()->username }}</span>
            <form method="POST" action="{{ route('logout') }}">
                @csrf
                <button type="submit" class="text-red-600 hover:text-red-800">Cerrar Sesión</button>
            </form>
        </div>
        @endauth
    </div>
</nav>