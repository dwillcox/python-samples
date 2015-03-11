program markov_chain
  implicit none
  integer, parameter :: N = 1000000
  integer :: i,j
  real :: start_time, end_time
  double precision, dimension(:,:), allocatable :: ave, std
  double precision, dimension(:,:), allocatable :: m
  double precision, dimension(:,:), allocatable :: xini
  double precision, dimension(:,:), allocatable :: mx

  call cpu_time(start_time)
  allocate(m(3,3))
  allocate(xini(3,1))
  allocate(mx(3,N))
  allocate(ave(3,1))
  allocate(std(3,1))

  m = transpose(reshape((/0.1, 0.2, 0.3, 0.7, 0.2, 0.5, 0.2, 0.6, 0.2/),shape(m)))
  xini = reshape((/1.0, 0.0, 0.0/),shape(xini))
  ave = reshape((/0.0, 0.0, 0.0/),shape(ave))
  std = reshape((/0.0, 0.0, 0.0/),shape(std))

  mx(:,1) = xini(:,1)
  do i=2,N
     ! Use either the intrinsic matmul function or the BLAS dgemv subroutine
     !mx(:,i) = matmul(m,mx(:,i-1))
     call dgemv('n',3,3,1.0d0,m,3,mx(:,i-1),1,0.0,mx(:,i),1)
     ave(:,1) = ave(:,1) + mx(:,i)
  end do
  ave(:,1) = ave(:,1)/(N-1)

  do i=2,N
     std(:,1) = std(:,1) + ((mx(:,i)-ave(:,1))**2)
  end do

  std(:,1) = std(:,1)/(N-1)

  do j=1,3
     std(j,1) = std(j,1)**(0.5)
  end do
  
  call cpu_time(end_time)

!! Print the elements of matrix mx
!  write(*,*) "Matrix mx: "
!  do i=1,3
!     write(*,*) (mx(i,j), j = 1,N)
!  end do

  write(*,*) "Iterations: ", N

  write(*,*) "Initial State: "
  do i=1,3
     write(*,*) (xini(i,1))
  end do

  write(*,*) "Average State: "
  do i=1,3
     write(*,*) (ave(i,1))
  end do

  write(*,*) "State Standard Deviation: "
  do i=1,3
     write(*,*) (std(i,1))
  end do

  write(*,*) "--------------------------------"
  write(*,*) "Time elapsed: ", end_time-start_time, " seconds"

  deallocate(m)
  deallocate(xini)
  deallocate(mx)
  deallocate(ave)
  deallocate(std)

end program
