<?php

namespace Generated;

/**
 * Class representing DetalleSurtidoType
 *
 * 
 * XSD Type: DetalleSurtidoType
 */
class DetalleSurtidoType
{
    /**
     * Tipo complejo que representa cada línea del detalle del surtido
     *
     * @var \Generated\LineaDetalleSurtidoType[] $lineaDetalleSurtido
     */
    private $lineaDetalleSurtido = [
        
    ];

    /**
     * Adds as lineaDetalleSurtido
     *
     * Tipo complejo que representa cada línea del detalle del surtido
     *
     * @return self
     * @param \Generated\LineaDetalleSurtidoType $lineaDetalleSurtido
     */
    public function addToLineaDetalleSurtido(\Generated\LineaDetalleSurtidoType $lineaDetalleSurtido)
    {
        $this->lineaDetalleSurtido[] = $lineaDetalleSurtido;
        return $this;
    }

    /**
     * isset lineaDetalleSurtido
     *
     * Tipo complejo que representa cada línea del detalle del surtido
     *
     * @param int|string $index
     * @return bool
     */
    public function issetLineaDetalleSurtido($index)
    {
        return isset($this->lineaDetalleSurtido[$index]);
    }

    /**
     * unset lineaDetalleSurtido
     *
     * Tipo complejo que representa cada línea del detalle del surtido
     *
     * @param int|string $index
     * @return void
     */
    public function unsetLineaDetalleSurtido($index)
    {
        unset($this->lineaDetalleSurtido[$index]);
    }

    /**
     * Gets as lineaDetalleSurtido
     *
     * Tipo complejo que representa cada línea del detalle del surtido
     *
     * @return \Generated\LineaDetalleSurtidoType[]
     */
    public function getLineaDetalleSurtido()
    {
        return $this->lineaDetalleSurtido;
    }

    /**
     * Sets a new lineaDetalleSurtido
     *
     * Tipo complejo que representa cada línea del detalle del surtido
     *
     * @param \Generated\LineaDetalleSurtidoType[] $lineaDetalleSurtido
     * @return self
     */
    public function setLineaDetalleSurtido(array $lineaDetalleSurtido)
    {
        $this->lineaDetalleSurtido = $lineaDetalleSurtido;
        return $this;
    }
}

