<?php

namespace Generated;

/**
 * Class representing CodigoMonedaType
 *
 * 
 * XSD Type: CodigoMonedaType
 */
class CodigoMonedaType
{
    /**
     * Código de la moneda
     *
     * @var string $codigoMoneda
     */
    private $codigoMoneda = null;

    /**
     * Tipo de cambio
     *
     * @var float $tipoCambio
     */
    private $tipoCambio = null;

    /**
     * Gets as codigoMoneda
     *
     * Código de la moneda
     *
     * @return string
     */
    public function getCodigoMoneda()
    {
        return $this->codigoMoneda;
    }

    /**
     * Sets a new codigoMoneda
     *
     * Código de la moneda
     *
     * @param string $codigoMoneda
     * @return self
     */
    public function setCodigoMoneda($codigoMoneda)
    {
        $this->codigoMoneda = $codigoMoneda;
        return $this;
    }

    /**
     * Gets as tipoCambio
     *
     * Tipo de cambio
     *
     * @return float
     */
    public function getTipoCambio()
    {
        return $this->tipoCambio;
    }

    /**
     * Sets a new tipoCambio
     *
     * Tipo de cambio
     *
     * @param float $tipoCambio
     * @return self
     */
    public function setTipoCambio($tipoCambio)
    {
        $this->tipoCambio = $tipoCambio;
        return $this;
    }
}

