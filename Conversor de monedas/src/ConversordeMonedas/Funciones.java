package ConversordeMonedas;

import javax.swing.JOptionPane;

public class Funciones {

	ConvertirMonedas monedas = new ConvertirMonedas();
	ConvertirMonedasABolivianos boliviano = new ConvertirMonedasABolivianos();
	
    public void ConvertirMonedas(double Minput) {
    	String opcion = (JOptionPane.showInputDialog(null, 
    			"Elije la moneda a la que deseas convertir tu dinero ", "Monedas", 
    			JOptionPane.PLAIN_MESSAGE, null, new Object[] 
    			{"De Boliviano a Dólar", "De Boliviano a Euro", "De Boliviano a Libras","De Boliviano a Yen","De Boliviano a Won Coreano","De Dólar a Boliviano", "De Euro a Boliviano", "De Libras a Boliviano","De Yen a Boliviano","De Won Coreano a Boliviano"}, 
    			"Seleccion")).toString();
        switch(opcion) {
        case "De Boliviano a Dólar":
        	monedas.ConvertirBolivianosADolares(Minput);
        	break;
        case "De Boliviano a Euro":
        	monedas.ConvertirBolivianosAEuros(Minput);
        	break;
        case "De Boliviano a Libras":
        	monedas.ConvertirBolivianosALibras(Minput);
        	break;
        case "De Boliviano a Yen":
        	monedas.ConvertirBolivianosAYen(Minput);
        	break;
        case "De Boliviano a Won Coreano":
        	monedas.ConvertirBolivianosAWon(Minput);
        	break;    	    	                          
        case "De Dólar a Boliviano":
        	boliviano.ConvertirDolaresABolivianos(Minput);
        	break;
        case "De Euro a Boliviano":
        	boliviano.ConvertirEurosABolivianos(Minput);
        	break;
        case "De Libras a Boliviano":
        	boliviano.ConvertirLibrasABolivianos(Minput);
        	break;
        case "De Yen a Boliviano":
        	boliviano.ConvertirYenABolivianos(Minput);
        	break;
        case "De Won Coreano a Boliviano":
            boliviano.ConvertirWonABolivianos(Minput);
            break;
        }      
    }
        
}
