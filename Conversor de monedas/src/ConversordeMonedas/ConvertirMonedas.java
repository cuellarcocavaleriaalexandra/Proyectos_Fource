package ConversordeMonedas;

import javax.swing.JOptionPane;

public class ConvertirMonedas {

	
	public void ConvertirBolivianosADolares(double valor) {
		double monedaDolar = valor / 6.92;
		monedaDolar = (double) Math.round(monedaDolar *100d)/100;
        JOptionPane.showMessageDialog(null, "Tienes $ " +monedaDolar+ " Dolares");
	}
	
	public void ConvertirBolivianosAEuros(double valor) {
		double monedaEuro = valor / 7.33;
		monedaEuro = (double) Math.round(monedaEuro *100d)/100;
		JOptionPane.showMessageDialog(null, "Tienes $ " +monedaEuro+ " Euros");
	}
	
	public void ConvertirBolivianosALibras(double valor) {
		double monedaLibra = valor / 8.45;
        monedaLibra = (double) Math.round(monedaLibra *100d)/100;
        JOptionPane.showMessageDialog(null, "Tienes $ " +monedaLibra+ " Libras Esterlinas");
	}
	
	public void ConvertirBolivianosAYen(double valor) {
		double monedaYen = valor / 0.046;
        monedaYen = (double) Math.round(monedaYen *100d)/100;
        JOptionPane.showMessageDialog(null, "Tienes $ " +monedaYen+ " Yuanes");
	}
	
	public void ConvertirBolivianosAWon(double valor) {
		double monedaWon = valor / 0.0051;
        monedaWon = (double) Math.round(monedaWon *100d)/100;
        JOptionPane.showMessageDialog(null, "Tienes $ " +monedaWon+ " Wons");
	}
}
