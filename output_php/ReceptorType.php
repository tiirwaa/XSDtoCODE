<?php

namespace Generated;

/**
 * Class representing ReceptorType
 *
 * 
 * XSD Type: ReceptorType
 */
class ReceptorType
{
    /**
     * Nombre o razon social
     *
     * @var string $nombre
     */
    private $nombre = null;

    /**
     * @var \Generated\IdentificacionType $identificacion
     */
    private $identificacion = null;

    /**
     * En caso de que se cuente con nombre comercial debe indicarse
     *
     * @var string $nombreComercial
     */
    private $nombreComercial = null;

    /**
     * @var \Generated\UbicacionType $ubicacion
     */
    private $ubicacion = null;

    /**
     * Campo para incluir la direccion del extranjero, en caso de requerirse.
     *
     * @var string $otrasSenasExtranjero
     */
    private $otrasSenasExtranjero = null;

    /**
     * @var \Generated\TelefonoType $telefono
     */
    private $telefono = null;

    /**
     * Este campo será de condición obligatoria, cuando el cliente lo requiera. Debe cumplir con la siguiente estructura: 
     *  \s*\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*\s*
     *
     * @var string $correoElectronico
     */
    private $correoElectronico = null;

    /**
     * Gets as nombre
     *
     * Nombre o razon social
     *
     * @return string
     */
    public function getNombre()
    {
        return $this->nombre;
    }

    /**
     * Sets a new nombre
     *
     * Nombre o razon social
     *
     * @param string $nombre
     * @return self
     */
    public function setNombre($nombre)
    {
        $this->nombre = $nombre;
        return $this;
    }

    /**
     * Gets as identificacion
     *
     * @return \Generated\IdentificacionType
     */
    public function getIdentificacion()
    {
        return $this->identificacion;
    }

    /**
     * Sets a new identificacion
     *
     * @param \Generated\IdentificacionType $identificacion
     * @return self
     */
    public function setIdentificacion(\Generated\IdentificacionType $identificacion)
    {
        $this->identificacion = $identificacion;
        return $this;
    }

    /**
     * Gets as nombreComercial
     *
     * En caso de que se cuente con nombre comercial debe indicarse
     *
     * @return string
     */
    public function getNombreComercial()
    {
        return $this->nombreComercial;
    }

    /**
     * Sets a new nombreComercial
     *
     * En caso de que se cuente con nombre comercial debe indicarse
     *
     * @param string $nombreComercial
     * @return self
     */
    public function setNombreComercial($nombreComercial)
    {
        $this->nombreComercial = $nombreComercial;
        return $this;
    }

    /**
     * Gets as ubicacion
     *
     * @return \Generated\UbicacionType
     */
    public function getUbicacion()
    {
        return $this->ubicacion;
    }

    /**
     * Sets a new ubicacion
     *
     * @param \Generated\UbicacionType $ubicacion
     * @return self
     */
    public function setUbicacion(?\Generated\UbicacionType $ubicacion = null)
    {
        $this->ubicacion = $ubicacion;
        return $this;
    }

    /**
     * Gets as otrasSenasExtranjero
     *
     * Campo para incluir la direccion del extranjero, en caso de requerirse.
     *
     * @return string
     */
    public function getOtrasSenasExtranjero()
    {
        return $this->otrasSenasExtranjero;
    }

    /**
     * Sets a new otrasSenasExtranjero
     *
     * Campo para incluir la direccion del extranjero, en caso de requerirse.
     *
     * @param string $otrasSenasExtranjero
     * @return self
     */
    public function setOtrasSenasExtranjero($otrasSenasExtranjero)
    {
        $this->otrasSenasExtranjero = $otrasSenasExtranjero;
        return $this;
    }

    /**
     * Gets as telefono
     *
     * @return \Generated\TelefonoType
     */
    public function getTelefono()
    {
        return $this->telefono;
    }

    /**
     * Sets a new telefono
     *
     * @param \Generated\TelefonoType $telefono
     * @return self
     */
    public function setTelefono(?\Generated\TelefonoType $telefono = null)
    {
        $this->telefono = $telefono;
        return $this;
    }

    /**
     * Gets as correoElectronico
     *
     * Este campo será de condición obligatoria, cuando el cliente lo requiera. Debe cumplir con la siguiente estructura: 
     *  \s*\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*\s*
     *
     * @return string
     */
    public function getCorreoElectronico()
    {
        return $this->correoElectronico;
    }

    /**
     * Sets a new correoElectronico
     *
     * Este campo será de condición obligatoria, cuando el cliente lo requiera. Debe cumplir con la siguiente estructura: 
     *  \s*\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*\s*
     *
     * @param string $correoElectronico
     * @return self
     */
    public function setCorreoElectronico($correoElectronico)
    {
        $this->correoElectronico = $correoElectronico;
        return $this;
    }
}

