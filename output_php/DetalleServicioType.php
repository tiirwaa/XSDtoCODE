<?php

namespace Generated;

/**
 * Class representing DetalleServicioType
 *
 * 
 * XSD Type: DetalleServicioType
 */
class DetalleServicioType
{
    /**
     * Cada línea del detalle de la mercancia o servicio prestado.
     *
     * @var \Generated\LineaDetalleType[] $lineaDetalle
     */
    private $lineaDetalle = [
        
    ];

    /**
     * Adds as lineaDetalle
     *
     * Cada línea del detalle de la mercancia o servicio prestado.
     *
     * @return self
     * @param \Generated\LineaDetalleType $lineaDetalle
     */
    public function addToLineaDetalle(\Generated\LineaDetalleType $lineaDetalle)
    {
        $this->lineaDetalle[] = $lineaDetalle;
        return $this;
    }

    /**
     * isset lineaDetalle
     *
     * Cada línea del detalle de la mercancia o servicio prestado.
     *
     * @param int|string $index
     * @return bool
     */
    public function issetLineaDetalle($index)
    {
        return isset($this->lineaDetalle[$index]);
    }

    /**
     * unset lineaDetalle
     *
     * Cada línea del detalle de la mercancia o servicio prestado.
     *
     * @param int|string $index
     * @return void
     */
    public function unsetLineaDetalle($index)
    {
        unset($this->lineaDetalle[$index]);
    }

    /**
     * Gets as lineaDetalle
     *
     * Cada línea del detalle de la mercancia o servicio prestado.
     *
     * @return \Generated\LineaDetalleType[]
     */
    public function getLineaDetalle()
    {
        return $this->lineaDetalle;
    }

    /**
     * Sets a new lineaDetalle
     *
     * Cada línea del detalle de la mercancia o servicio prestado.
     *
     * @param \Generated\LineaDetalleType[] $lineaDetalle
     * @return self
     */
    public function setLineaDetalle(array $lineaDetalle)
    {
        $this->lineaDetalle = $lineaDetalle;
        return $this;
    }
}

