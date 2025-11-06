<?php

namespace Generated;

/**
 * Class representing MedioPagoType
 *
 * 
 * XSD Type: MedioPagoType
 */
class MedioPagoType
{
    /**
     * Corresponde al medio de pago empleado: 01 - Efectivo, 02 - Tarjeta, 03 - Cheque, 04 - Transferencia - depósito bancario, 05 - Recaudado por terceros, 06 - SINPE MOVIL, 07 - Plataforma Digital, 99 - Otros
     *
     * @var string $tipoMedioPago
     */
    private $tipoMedioPago = null;

    /**
     * Será obligatorio en caso de utilizar el código 99 de "Otros" de la nota 6. Se debe describir puntualmente el medio de pago utilizado
     *
     * @var string $medioPagoOtros
     */
    private $medioPagoOtros = null;

    /**
     * Se deberá detallar el monto correspondiente al tipo de pago seleccionado. Se volverá obligatorio cuando se utilice más de un medio de pago.
     *
     * @var float $totalMedioPago
     */
    private $totalMedioPago = null;

    /**
     * Gets as tipoMedioPago
     *
     * Corresponde al medio de pago empleado: 01 - Efectivo, 02 - Tarjeta, 03 - Cheque, 04 - Transferencia - depósito bancario, 05 - Recaudado por terceros, 06 - SINPE MOVIL, 07 - Plataforma Digital, 99 - Otros
     *
     * @return string
     */
    public function getTipoMedioPago()
    {
        return $this->tipoMedioPago;
    }

    /**
     * Sets a new tipoMedioPago
     *
     * Corresponde al medio de pago empleado: 01 - Efectivo, 02 - Tarjeta, 03 - Cheque, 04 - Transferencia - depósito bancario, 05 - Recaudado por terceros, 06 - SINPE MOVIL, 07 - Plataforma Digital, 99 - Otros
     *
     * @param string $tipoMedioPago
     * @return self
     */
    public function setTipoMedioPago($tipoMedioPago)
    {
        $this->tipoMedioPago = $tipoMedioPago;
        return $this;
    }

    /**
     * Gets as medioPagoOtros
     *
     * Será obligatorio en caso de utilizar el código 99 de "Otros" de la nota 6. Se debe describir puntualmente el medio de pago utilizado
     *
     * @return string
     */
    public function getMedioPagoOtros()
    {
        return $this->medioPagoOtros;
    }

    /**
     * Sets a new medioPagoOtros
     *
     * Será obligatorio en caso de utilizar el código 99 de "Otros" de la nota 6. Se debe describir puntualmente el medio de pago utilizado
     *
     * @param string $medioPagoOtros
     * @return self
     */
    public function setMedioPagoOtros($medioPagoOtros)
    {
        $this->medioPagoOtros = $medioPagoOtros;
        return $this;
    }

    /**
     * Gets as totalMedioPago
     *
     * Se deberá detallar el monto correspondiente al tipo de pago seleccionado. Se volverá obligatorio cuando se utilice más de un medio de pago.
     *
     * @return float
     */
    public function getTotalMedioPago()
    {
        return $this->totalMedioPago;
    }

    /**
     * Sets a new totalMedioPago
     *
     * Se deberá detallar el monto correspondiente al tipo de pago seleccionado. Se volverá obligatorio cuando se utilice más de un medio de pago.
     *
     * @param float $totalMedioPago
     * @return self
     */
    public function setTotalMedioPago($totalMedioPago)
    {
        $this->totalMedioPago = $totalMedioPago;
        return $this;
    }
}

